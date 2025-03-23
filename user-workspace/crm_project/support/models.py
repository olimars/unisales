from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

class TicketCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Ticket Categories'

    def __str__(self):
        return self.name

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    SOURCE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('web', 'Web Portal'),
        ('chat', 'Chat'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='tickets')
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='web')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.contact.email}"

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)  # True for internal notes, False for customer-visible comments

    def __str__(self):
        return f"Comment on {self.ticket.title}"

class KnowledgeBaseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Knowledge Base Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(KnowledgeBaseCategory, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class ArticleAttachment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='knowledge_base/attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # Size in bytes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
