from django.contrib import admin
from .models import Contact, Interaction

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'company', 'created_at', 'assigned_to')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Company Information', {
            'fields': ('company', 'position')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('contact', 'type', 'subject', 'created_by', 'created_at')
    list_filter = ('type', 'created_at', 'created_by')
    search_fields = ('subject', 'notes', 'contact__first_name', 'contact__last_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Interaction Details', {
            'fields': ('contact', 'type', 'subject', 'notes')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new interaction
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
