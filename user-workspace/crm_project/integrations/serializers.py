from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from contacts.serializers import UserSerializer
from .models import Integration, Webhook, SyncLog, DataMapping, ExternalReference

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = [
            'id', 'integration', 'event_type', 'url',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'secret_key': {'write_only': True}
        }

class SyncLogSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = SyncLog
        fields = [
            'id', 'integration', 'status', 'start_time',
            'end_time', 'records_processed', 'records_succeeded',
            'records_failed', 'error_message', 'details',
            'success_rate', 'duration'
        ]

    def get_success_rate(self, obj):
        if obj.records_processed == 0:
            return 0
        return round((obj.records_succeeded / obj.records_processed) * 100, 2)

    def get_duration(self, obj):
        if obj.end_time and obj.start_time:
            duration = obj.end_time - obj.start_time
            return duration.total_seconds()
        return None

class DataMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMapping
        fields = [
            'id', 'integration', 'source_model', 'target_model',
            'mapping_type', 'source_field', 'target_field',
            'transformation_rule', 'is_required',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ExternalReferenceSerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    object_repr = serializers.SerializerMethodField()

    class Meta:
        model = ExternalReference
        fields = [
            'id', 'integration', 'content_type',
            'content_type_name', 'object_id', 'object_repr',
            'external_id', 'external_url', 'last_synced',
            'metadata'
        ]
        read_only_fields = ['last_synced']

    def get_content_type_name(self, obj):
        return obj.content_type.model_class().__name__

    def get_object_repr(self, obj):
        return str(obj.content_object)

class IntegrationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    webhooks = WebhookSerializer(many=True, read_only=True)
    data_mappings = DataMappingSerializer(many=True, read_only=True)
    sync_logs = SyncLogSerializer(many=True, read_only=True)
    latest_sync = serializers.SerializerMethodField()
    sync_status = serializers.SerializerMethodField()

    class Meta:
        model = Integration
        fields = [
            'id', 'name', 'integration_type', 'provider',
            'status', 'configuration', 'webhook_url',
            'created_by', 'webhooks', 'data_mappings',
            'sync_logs', 'latest_sync', 'sync_status',
            'last_sync', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_sync']
        extra_kwargs = {
            'credentials': {'write_only': True},
            'api_key': {'write_only': True}
        }

    def get_latest_sync(self, obj):
        latest_sync = obj.sync_logs.order_by('-start_time').first()
        if latest_sync:
            return SyncLogSerializer(latest_sync).data
        return None

    def get_sync_status(self, obj):
        latest_sync = obj.sync_logs.order_by('-start_time').first()
        if not latest_sync:
            return 'never_synced'
        if not latest_sync.end_time:
            return 'syncing'
        return latest_sync.status

class IntegrationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    created_by = UserSerializer(read_only=True)
    sync_status = serializers.SerializerMethodField()
    webhook_count = serializers.SerializerMethodField()

    class Meta:
        model = Integration
        fields = [
            'id', 'name', 'integration_type', 'provider',
            'status', 'created_by', 'sync_status',
            'webhook_count', 'last_sync', 'created_at'
        ]

    def get_sync_status(self, obj):
        latest_sync = obj.sync_logs.order_by('-start_time').first()
        if not latest_sync:
            return 'never_synced'
        if not latest_sync.end_time:
            return 'syncing'
        return latest_sync.status

    def get_webhook_count(self, obj):
        return obj.webhooks.count()

class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentType model to help with integration mappings
    """
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']