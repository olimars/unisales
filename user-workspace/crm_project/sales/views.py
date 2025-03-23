from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Pipeline, Stage, Opportunity, Activity
from .serializers import (
    PipelineSerializer,
    StageSerializer,
    OpportunitySerializer,
    OpportunityListSerializer,
    ActivitySerializer
)

class PipelineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing sales pipelines.
    """
    permission_classes = [IsAuthenticated]
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

    @action(detail=True, methods=['get'])
    def stages(self, request, pk=None):
        """
        Get all stages for a specific pipeline.
        """
        pipeline = self.get_object()
        stages = pipeline.stages.all().order_by('order')
        serializer = StageSerializer(stages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get pipeline statistics.
        """
        pipeline = self.get_object()
        stages = pipeline.stages.all()
        
        stats = []
        for stage in stages:
            opportunities = stage.opportunities.all()
            stats.append({
                'stage_name': stage.name,
                'opportunity_count': opportunities.count(),
                'total_value': opportunities.aggregate(
                    total=Sum('amount')
                )['total'] or 0
            })
        
        return Response(stats)

class StageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing pipeline stages.
    """
    permission_classes = [IsAuthenticated]
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pipeline']

class OpportunityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing opportunities.
    """
    permission_classes = [IsAuthenticated]
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stage', 'priority', 'assigned_to']
    search_fields = ['title', 'contact__first_name', 'contact__last_name', 'contact__company']
    ordering_fields = ['created_at', 'expected_close_date', 'amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return OpportunityListSerializer
        return OpportunitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only assigned opportunities
        if not user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True)
            )

        return queryset

    def perform_create(self, serializer):
        if not serializer.validated_data.get('assigned_to'):
            serializer.validated_data['assigned_to'] = self.request.user
        serializer.save()

    @action(detail=True, methods=['post'])
    def change_stage(self, request, pk=None):
        """
        Change the stage of an opportunity.
        """
        opportunity = self.get_object()
        stage_id = request.data.get('stage_id')
        
        try:
            new_stage = Stage.objects.get(pk=stage_id)
            opportunity.stage = new_stage
            opportunity.save()
            serializer = self.get_serializer(opportunity)
            return Response(serializer.data)
        except Stage.DoesNotExist:
            return Response(
                {'error': 'Stage not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get sales dashboard statistics.
        """
        queryset = self.get_queryset()
        
        # Calculate various metrics
        total_value = queryset.aggregate(total=Sum('amount'))['total'] or 0
        open_opportunities = queryset.count()
        
        # This month's opportunities
        this_month = timezone.now().replace(day=1)
        this_month_opps = queryset.filter(created_at__gte=this_month)
        this_month_value = this_month_opps.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Upcoming closing dates
        upcoming = queryset.filter(
            expected_close_date__gte=timezone.now(),
            expected_close_date__lte=timezone.now() + timedelta(days=30)
        ).count()
        
        return Response({
            'total_pipeline_value': total_value,
            'open_opportunities': open_opportunities,
            'this_month_value': this_month_value,
            'upcoming_closing': upcoming
        })

class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing activities.
    """
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'completed', 'opportunity', 'assigned_to']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only assigned activities
        if not user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=user) | 
                Q(assigned_to__isnull=True) |
                Q(opportunity__assigned_to=user)
            )

        return queryset

    def perform_create(self, serializer):
        if not serializer.validated_data.get('assigned_to'):
            serializer.validated_data['assigned_to'] = self.request.user
        serializer.save()

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Get upcoming activities.
        """
        activities = self.get_queryset().filter(
            completed=False,
            due_date__gte=timezone.now(),
            due_date__lte=timezone.now() + timedelta(days=7)
        ).order_by('due_date')
        
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
