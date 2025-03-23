from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    probability = models.PositiveIntegerField(default=0)  # Probability of closing (0-100)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.pipeline.name} - {self.name}"

class Opportunity(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='opportunities')
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='opportunities')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    expected_close_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.contact.first_name} {self.contact.last_name}"

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('task', 'Task'),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    subject = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.subject}"
