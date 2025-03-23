from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
        ('converted', 'Converted'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} with {self.contact} - {self.subject}"
