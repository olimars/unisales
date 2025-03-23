from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('sales_rep', 'Sales Representative'),
        ('support_agent', 'Support Agent'),
        ('marketing_user', 'Marketing User'),
    ]

    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_rep')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    theme_preference = models.CharField(max_length=10, choices=THEME_CHOICES, default='system')
    notification_preferences = models.JSONField(default=dict)
    dashboard_layout = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CompanySettings(models.Model):
    company_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company/', blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    time_zone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(max_length=50, default='YYYY-MM-DD')
    time_format = models.CharField(max_length=50, default='HH:mm:ss')
    currency = models.CharField(max_length=3, default='USD')
    fiscal_year_start = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Company Settings'

    def __str__(self):
        return self.company_name

class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=50)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.model_name}"

class CustomField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('boolean', 'Boolean'),
        ('select', 'Select'),
        ('multiselect', 'Multi-Select'),
    ]

    MODEL_CHOICES = [
        ('contact', 'Contact'),
        ('opportunity', 'Opportunity'),
        ('ticket', 'Ticket'),
        ('campaign', 'Campaign'),
    ]

    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES)
    options = models.JSONField(default=list)  # For select/multiselect fields
    is_required = models.BooleanField(default=False)
    default_value = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.model_name})"
