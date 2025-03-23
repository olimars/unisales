from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Integration(models.Model):
    INTEGRATION_TYPES = [
        ('email', 'Email Service'),
        ('calendar', 'Calendar Service'),
        ('storage', 'Storage Service'),
        ('payment', 'Payment Gateway'),
        ('social', 'Social Media'),
        ('chat', 'Chat Service'),
        ('erp', 'ERP System'),
        ('custom', 'Custom Integration'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('pending', 'Pending Configuration'),
    ]

    name = models.CharField(max_length=200)
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_TYPES)
    provider = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    configuration = models.JSONField(default=dict)  # Stores integration-specific settings
    credentials = models.JSONField(default=dict)  # Stores encrypted credentials
    webhook_url = models.URLField(blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_sync = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.provider}"

class Webhook(models.Model):
    EVENT_TYPES = [
        ('contact_created', 'Contact Created'),
        ('contact_updated', 'Contact Updated'),
        ('deal_created', 'Deal Created'),
        ('deal_updated', 'Deal Updated'),
        ('ticket_created', 'Ticket Created'),
        ('ticket_updated', 'Ticket Updated'),
        ('custom', 'Custom Event'),
    ]

    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='webhooks')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    url = models.URLField()
    secret_key = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.integration.name} - {self.event_type}"

class SyncLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('partial', 'Partial Success'),
    ]

    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='sync_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    records_processed = models.PositiveIntegerField(default=0)
    records_succeeded = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.integration.name} Sync - {self.start_time}"

class DataMapping(models.Model):
    MAPPING_TYPES = [
        ('field', 'Field Mapping'),
        ('value', 'Value Mapping'),
        ('function', 'Function Mapping'),
    ]

    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='data_mappings')
    source_model = models.CharField(max_length=100)  # e.g., 'Contact', 'Deal'
    target_model = models.CharField(max_length=100)  # External system's model name
    mapping_type = models.CharField(max_length=20, choices=MAPPING_TYPES)
    source_field = models.CharField(max_length=100)
    target_field = models.CharField(max_length=100)
    transformation_rule = models.TextField(blank=True)  # Optional transformation logic
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.integration.name} - {self.source_model}.{self.source_field} → {self.target_field}"

class ExternalReference(models.Model):
    """Stores references to external system IDs for synchronized records"""
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    
    # Generic foreign key to allow references for any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    external_id = models.CharField(max_length=255)
    external_url = models.URLField(blank=True)
    last_synced = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        unique_together = ['integration', 'content_type', 'object_id', 'external_id']
        indexes = [
            models.Index(fields=['integration', 'content_type', 'object_id']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.integration.name} - {self.content_object} - {self.external_id}"
