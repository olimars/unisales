from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dashboard, Widget, Report, ReportExport, Metric
from contacts.serializers import UserSerializer

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = [
            'id', 'dashboard', 'name', 'widget_type',
            'query', 'refresh_interval', 'position_x',
            'position_y', 'width', 'height',
            'configuration', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_query(self, value):
        """
        Validate that the query is safe and doesn't contain harmful SQL.
        """
        # Add query validation logic here
        forbidden_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'INSERT', 'UPDATE']
        if any(keyword in value.upper() for keyword in forbidden_keywords):
            raise serializers.ValidationError(
                "Query contains forbidden operations"
            )
        return value

class DashboardSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    widgets = WidgetSerializer(many=True, read_only=True)
    widget_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = [
            'id', 'name', 'description', 'created_by',
            'is_public', 'widgets', 'widget_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_widget_count(self, obj):
        return obj.widgets.count()

class DashboardListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    created_by = UserSerializer(read_only=True)
    widget_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = [
            'id', 'name', 'is_public', 'created_by',
            'widget_count', 'created_at'
        ]

    def get_widget_count(self, obj):
        return obj.widgets.count()

class ReportExportSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ReportExport
        fields = '__all__'
        read_only_fields = ['created_at']

class ReportSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    recipients = UserSerializer(many=True, read_only=True)
    recipient_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='recipients',
        write_only=True,
        many=True,
        required=False
    )
    exports = ReportExportSerializer(many=True, read_only=True)
    last_export = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'name', 'description', 'report_type',
            'query', 'parameters', 'created_by',
            'is_scheduled', 'schedule_type',
            'recipients', 'recipient_ids', 'exports',
            'last_export', 'last_run',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_run']

    def get_last_export(self, obj):
        last_export = obj.exports.order_by('-created_at').first()
        if last_export:
            return ReportExportSerializer(last_export).data
        return None

    def validate_query(self, value):
        """
        Validate that the query is safe and doesn't contain harmful SQL.
        """
        forbidden_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'INSERT', 'UPDATE']
        if any(keyword in value.upper() for keyword in forbidden_keywords):
            raise serializers.ValidationError(
                "Query contains forbidden operations"
            )
        return value

class ReportListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    created_by = UserSerializer(read_only=True)
    recipient_count = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'is_scheduled',
            'schedule_type', 'created_by', 'recipient_count',
            'last_run', 'created_at'
        ]

    def get_recipient_count(self, obj):
        return obj.recipients.count()

class MetricSerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    object_repr = serializers.SerializerMethodField()

    class Meta:
        model = Metric
        fields = [
            'id', 'name', 'description', 'content_type',
            'content_type_name', 'object_id', 'object_repr',
            'value', 'timestamp', 'metadata', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_content_type_name(self, obj):
        return obj.content_type.model_class().__name__

    def get_object_repr(self, obj):
        return str(obj.content_object)