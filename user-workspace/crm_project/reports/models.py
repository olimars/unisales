from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Widget(models.Model):
    WIDGET_TYPES = [
        ('line_chart', 'Line Chart'),
        ('bar_chart', 'Bar Chart'),
        ('pie_chart', 'Pie Chart'),
        ('metric', 'Single Metric'),
        ('table', 'Table'),
        ('funnel', 'Funnel'),
        ('kanban', 'Kanban Board'),
    ]

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    query = models.TextField()  # SQL or aggregation query
    refresh_interval = models.PositiveIntegerField(default=3600)  # in seconds
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    configuration = models.JSONField(default=dict)  # Store widget-specific configuration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_widget_type_display()}"

class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('marketing', 'Marketing Report'),
        ('support', 'Support Report'),
        ('activity', 'Activity Report'),
        ('custom', 'Custom Report'),
    ]

    SCHEDULE_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    query = models.TextField()  # SQL or aggregation query
    parameters = models.JSONField(default=dict)  # Store report parameters
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_scheduled = models.BooleanField(default=False)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES, null=True, blank=True)
    recipients = models.ManyToManyField(User, related_name='subscribed_reports', blank=True)
    last_run = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ReportExport(models.Model):
    EXPORT_FORMATS = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('pdf', 'PDF'),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='exports')
    format = models.CharField(max_length=10, choices=EXPORT_FORMATS)
    file = models.FileField(upload_to='reports/exports/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report.name} - {self.format} - {self.created_at}"

class Metric(models.Model):
    """Model for tracking various metrics and KPIs"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Generic foreign key to allow metrics for any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    value = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField()
    
    # Additional metadata
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.name} - {self.value} ({self.timestamp})"
