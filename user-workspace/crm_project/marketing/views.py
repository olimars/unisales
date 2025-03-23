from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from .models import Campaign, EmailTemplate, CampaignRecipient, AutomationWorkflow, AutomationStep
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    EmailTemplateSerializer,
    CampaignRecipientSerializer,
    AutomationWorkflowSerializer,
    AutomationWorkflowListSerializer,
    AutomationStepSerializer
)

class EmailTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing email templates.
    """
    permission_classes = [IsAuthenticated]
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'subject']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing campaigns.
    """
    permission_classes = [IsAuthenticated]
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CampaignListSerializer
        return CampaignSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_recipients(self, request, pk=None):
        """
        Add recipients to a campaign.
        """
        campaign = self.get_object()
        contact_ids = request.data.get('contact_ids', [])
        
        added_recipients = []
        existing_recipients = []
        
        for contact_id in contact_ids:
            recipient, created = CampaignRecipient.objects.get_or_create(
                campaign=campaign,
                contact_id=contact_id
            )
            if created:
                added_recipients.append(recipient)
            else:
                existing_recipients.append(recipient)
        
        return Response({
            'added': CampaignRecipientSerializer(added_recipients, many=True).data,
            'existing': len(existing_recipients)
        })

    @action(detail=True, methods=['post'])
    def launch(self, request, pk=None):
        """
        Launch a campaign.
        """
        campaign = self.get_object()
        if campaign.status != 'draft':
            return Response(
                {'error': 'Campaign can only be launched from draft status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        campaign.status = 'active'
        campaign.start_date = timezone.now()
        campaign.save()
        
        # Here you would typically trigger your email sending logic
        
        return Response({'status': 'Campaign launched successfully'})

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get campaign statistics.
        """
        campaign = self.get_object()
        recipients = campaign.recipients.all()
        
        stats = {
            'total_recipients': recipients.count(),
            'sent': recipients.filter(status='sent').count(),
            'opened': recipients.filter(status='opened').count(),
            'clicked': recipients.filter(status='clicked').count(),
            'bounced': recipients.filter(status='bounced').count(),
            'unsubscribed': recipients.filter(status='unsubscribed').count(),
        }
        
        if stats['sent'] > 0:
            stats['open_rate'] = (stats['opened'] / stats['sent']) * 100
            stats['click_rate'] = (stats['clicked'] / stats['sent']) * 100
        else:
            stats['open_rate'] = 0
            stats['click_rate'] = 0
            
        return Response(stats)

class AutomationWorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing automation workflows.
    """
    permission_classes = [IsAuthenticated]
    queryset = AutomationWorkflow.objects.all()
    serializer_class = AutomationWorkflowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return AutomationWorkflowListSerializer
        return AutomationWorkflowSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'steps': request.data.get('steps', [])}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Toggle workflow status between active and inactive.
        """
        workflow = self.get_object()
        workflow.status = 'inactive' if workflow.status == 'active' else 'active'
        workflow.save()
        serializer = self.get_serializer(workflow)
        return Response(serializer.data)

class AutomationStepViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing automation steps.
    """
    permission_classes = [IsAuthenticated]
    queryset = AutomationStep.objects.all()
    serializer_class = AutomationStepSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workflow', 'trigger_type', 'action_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        workflow_id = self.request.query_params.get('workflow', None)
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        return queryset.order_by('order')
