from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('social', 'Social Media'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CampaignRecipient(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('unsubscribed', 'Unsubscribed'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='recipients')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['campaign', 'contact']

    def __str__(self):
        return f"{self.campaign.name} - {self.contact.email}"

class AutomationWorkflow(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AutomationStep(models.Model):
    TRIGGER_TYPES = [
        ('contact_created', 'Contact Created'),
        ('contact_updated', 'Contact Updated'),
        ('deal_stage_changed', 'Deal Stage Changed'),
        ('form_submitted', 'Form Submitted'),
        ('email_opened', 'Email Opened'),
        ('email_clicked', 'Email Clicked'),
    ]

    ACTION_TYPES = [
        ('send_email', 'Send Email'),
        ('update_contact', 'Update Contact'),
        ('create_task', 'Create Task'),
        ('notify_user', 'Notify User'),
    ]

    workflow = models.ForeignKey(AutomationWorkflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=200)
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    delay = models.PositiveIntegerField(default=0)  # Delay in minutes
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workflow.name} - {self.name}"
