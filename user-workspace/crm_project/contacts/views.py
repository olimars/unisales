from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Contact, Interaction
from .serializers import (
    ContactSerializer,
    ContactListSerializer,
    InteractionSerializer
)

class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing contacts.
    """
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    ordering_fields = ['created_at', 'updated_at', 'first_name', 'last_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return ContactListSerializer
        return ContactSerializer

    def get_queryset(self):
        """
        Filter contacts based on user's role and permissions.
        """
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only assigned contacts
        if not user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True)
            )

        return queryset

    def perform_create(self, serializer):
        """
        Set the assigned_to field if not provided.
        """
        if not serializer.validated_data.get('assigned_to'):
            serializer.validated_data['assigned_to'] = self.request.user
        serializer.save()

    @action(detail=True, methods=['post'])
    def add_interaction(self, request, pk=None):
        """
        Add an interaction to a contact.
        """
        contact = self.get_object()
        serializer = InteractionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                contact=contact,
                created_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """
        List all interactions for a contact.
        """
        contact = self.get_object()
        interactions = contact.interactions.all().order_by('-created_at')
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get contact statistics.
        """
        total_contacts = Contact.objects.count()
        status_counts = Contact.objects.values('status').annotate(
            count=Count('id')
        )
        
        return Response({
            'total_contacts': total_contacts,
            'status_distribution': status_counts,
        })

class InteractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing interactions.
    """
    permission_classes = [IsAuthenticated]
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'contact']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Filter interactions based on user's role and permissions.
        """
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only interactions for assigned contacts
        if not user.is_staff:
            queryset = queryset.filter(
                Q(contact__assigned_to=user) | 
                Q(contact__assigned_to__isnull=True)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
