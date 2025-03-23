from django.contrib import admin
from .models import (
    TicketCategory,
    Ticket,
    TicketComment,
    KnowledgeBaseCategory,
    Article,
    ArticleAttachment
)

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'parent')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ('created_at', 'created_by')
    fields = ('content', 'is_internal', 'created_by', 'created_at')

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact', 'category', 'status', 'priority', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at', 'assigned_to')
    search_fields = ('title', 'description', 'contact__email', 'contact__first_name', 'contact__last_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    inlines = [TicketCommentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Ticket Information', {
            'fields': ('title', 'description', 'contact', 'category')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'priority', 'assigned_to', 'due_date')
        }),
        ('Source Information', {
            'fields': ('source',)
        }),
        ('Resolution', {
            'fields': ('resolved_at',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new ticket
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TicketComment):
                if not instance.created_by_id:
                    instance.created_by = request.user
            instance.save()
        formset.save_m2m()

@admin.register(KnowledgeBaseCategory)
class KnowledgeBaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'created_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'name')

    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'parent', 'order')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ArticleAttachmentInline(admin.TabularInline):
    model = ArticleAttachment
    extra = 1
    readonly_fields = ('file_size', 'created_at')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'view_count', 'created_by', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content', 'tags')
    readonly_fields = (
        'created_at', 'updated_at', 'created_by',
        'view_count', 'helpful_count', 'not_helpful_count'
    )
    inlines = [ArticleAttachmentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'content', 'category', 'tags')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'helpful_count', 'not_helpful_count'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new article
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ArticleAttachment)
class ArticleAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'article', 'file_size', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('filename', 'article__title')
    readonly_fields = ('file_size', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Attachment Information', {
            'fields': ('article', 'file', 'filename')
        }),
        ('System Fields', {
            'fields': ('file_size', 'created_at'),
            'classes': ('collapse',)
        }),
    )
