from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from .models import (
    TicketCategory,
    Ticket,
    TicketComment,
    KnowledgeBaseCategory,
    Article,
    ArticleAttachment
)
from .serializers import (
    TicketCategorySerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketCommentSerializer,
    KnowledgeBaseCategorySerializer,
    ArticleSerializer,
    ArticleListSerializer,
    ArticleAttachmentSerializer
)

class TicketCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing ticket categories.
    """
    permission_classes = [IsAuthenticated]
    queryset = TicketCategory.objects.filter(parent__isnull=True)
    serializer_class = TicketCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing tickets.
    """
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'assigned_to']
    search_fields = ['title', 'description', 'contact__email', 'contact__first_name', 'contact__last_name']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only assigned tickets
        if not user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=user) | Q(created_by=user)
            )

        return queryset

    def perform_create(self, serializer):
        if not serializer.validated_data.get('assigned_to'):
            serializer.validated_data['assigned_to'] = self.request.user
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a ticket.
        """
        ticket = self.get_object()
        serializer = TicketCommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                ticket=ticket,
                created_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """
        Change the status of a ticket.
        """
        ticket = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Ticket.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If marking as resolved, set resolved_at
        if new_status == 'resolved' and ticket.status != 'resolved':
            ticket.resolved_at = timezone.now()
        
        ticket.status = new_status
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get ticket statistics.
        """
        queryset = self.get_queryset()
        
        stats = {
            'total_tickets': queryset.count(),
            'status_distribution': dict(
                queryset.values('status')
                .annotate(count=Count('id'))
                .values_list('status', 'count')
            ),
            'priority_distribution': dict(
                queryset.values('priority')
                .annotate(count=Count('id'))
                .values_list('priority', 'count')
            ),
            'average_resolution_time': None  # Calculate average resolution time
        }
        
        # Calculate average resolution time for resolved tickets
        resolved_tickets = queryset.filter(
            status='resolved',
            resolved_at__isnull=False
        )
        if resolved_tickets.exists():
            from django.db.models import Avg, F
            avg_resolution_time = resolved_tickets.annotate(
                resolution_time=F('resolved_at') - F('created_at')
            ).aggregate(avg_time=Avg('resolution_time'))
            stats['average_resolution_time'] = avg_resolution_time['avg_time']
        
        return Response(stats)

class KnowledgeBaseCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing knowledge base categories.
    """
    permission_classes = [IsAuthenticated]
    queryset = KnowledgeBaseCategory.objects.filter(parent__isnull=True)
    serializer_class = KnowledgeBaseCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing knowledge base articles.
    """
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'content', 'tags']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            # For list view, only show published articles unless user is staff
            if not self.request.user.is_staff:
                queryset = queryset.filter(is_published=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_publish(self, request, pk=None):
        """
        Toggle the published status of an article.
        """
        article = self.get_object()
        article.is_published = not article.is_published
        if article.is_published and not article.published_at:
            article.published_at = timezone.now()
        article.save()
        
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def record_view(self, request, pk=None):
        """
        Record a view of the article.
        """
        article = self.get_object()
        article.view_count += 1
        article.save()
        return Response({'status': 'view recorded'})

    @action(detail=True, methods=['post'])
    def record_feedback(self, request, pk=None):
        """
        Record helpful/not helpful feedback for the article.
        """
        article = self.get_object()
        feedback = request.data.get('feedback')
        
        if feedback == 'helpful':
            article.helpful_count += 1
        elif feedback == 'not_helpful':
            article.not_helpful_count += 1
        else:
            return Response(
                {'error': 'Invalid feedback'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        article.save()
        return Response({'status': 'feedback recorded'})
