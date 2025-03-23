from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Integration, Webhook, SyncLog, DataMapping, ExternalReference
from .serializers import (
    IntegrationSerializer,
    IntegrationListSerializer,
    WebhookSerializer,
    SyncLogSerializer,
    DataMappingSerializer,
    ExternalReferenceSerializer,
    ContentTypeSerializer
)

class IntegrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing integrations.
    """
    permission_classes = [IsAuthenticated]
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['integration_type', 'provider', 'status']
    search_fields = ['name', 'provider']

    def get_serializer_class(self):
        if self.action == 'list':
            return IntegrationListSerializer
        return IntegrationSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """
        Test the integration connection.
        """
        integration = self.get_object()
        
        # Here you would implement the actual connection test logic
        # based on the integration type and provider
        
        try:
            # Simulate connection test
            success = True
            message = "Connection successful"
            
            return Response({
                'success': success,
                'message': message
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """
        Trigger a sync for the integration.
        """
        integration = self.get_object()
        
        # Create sync log
        sync_log = SyncLog.objects.create(
            integration=integration,
            status='success',  # This would be updated based on actual sync result
            start_time=timezone.now()
        )
        
        try:
            # Here you would implement the actual sync logic
            # based on the integration type and provider
            
            # Update sync log with results
            sync_log.end_time = timezone.now()
            sync_log.records_processed = 0  # Update with actual count
            sync_log.records_succeeded = 0  # Update with actual count
            sync_log.save()
            
            # Update integration last sync time
            integration.last_sync = sync_log.end_time
            integration.save()
            
            return Response(SyncLogSerializer(sync_log).data)
        except Exception as e:
            sync_log.status = 'error'
            sync_log.error_message = str(e)
            sync_log.end_time = timezone.now()
            sync_log.save()
            
            return Response({
                'error': str(e),
                'sync_log': SyncLogSerializer(sync_log).data
            }, status=status.HTTP_400_BAD_REQUEST)

class WebhookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing webhooks.
    """
    permission_classes = [IsAuthenticated]
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['integration', 'event_type', 'is_active']

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """
        Test the webhook by sending a test payload.
        """
        webhook = self.get_object()
        
        try:
            # Here you would implement the actual webhook test
            # by sending a test payload to the webhook URL
            
            return Response({
                'success': True,
                'message': 'Test webhook sent successfully'
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class DataMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing data mappings.
    """
    permission_classes = [IsAuthenticated]
    queryset = DataMapping.objects.all()
    serializer_class = DataMappingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['integration', 'source_model', 'mapping_type']

    @action(detail=False, methods=['get'])
    def available_models(self, request):
        """
        Get list of available models for mapping.
        """
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def test_mapping(self, request, pk=None):
        """
        Test the data mapping with sample data.
        """
        mapping = self.get_object()
        sample_data = request.data.get('sample_data')
        
        try:
            # Here you would implement the actual mapping test
            # by applying the transformation rules to the sample data
            
            return Response({
                'success': True,
                'transformed_data': sample_data  # Replace with actual transformed data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class SyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing sync logs.
    """
    permission_classes = [IsAuthenticated]
    queryset = SyncLog.objects.all()
    serializer_class = SyncLogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['integration', 'status']
    ordering_fields = ['start_time', 'end_time']
    ordering = ['-start_time']

class ExternalReferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing external references.
    """
    permission_classes = [IsAuthenticated]
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['integration', 'content_type']

    @action(detail=True, methods=['get'])
    def sync_status(self, request, pk=None):
        """
        Get the sync status of an external reference.
        """
        reference = self.get_object()
        
        return Response({
            'last_synced': reference.last_synced,
            'external_id': reference.external_id,
            'external_url': reference.external_url,
            'metadata': reference.metadata
        })
