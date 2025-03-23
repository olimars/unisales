from django.contrib import admin
from .models import Campaign, EmailTemplate, CampaignRecipient, AutomationWorkflow, AutomationStep

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'start_date', 'end_date', 'created_by')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Campaign Information', {
            'fields': ('name', 'description', 'type', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Budget', {
            'fields': ('budget',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new campaign
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_by', 'created_at')
    search_fields = ('name', 'subject', 'content')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'subject', 'content')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new template
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'contact', 'status', 'sent_at', 'opened_at')
    list_filter = ('status', 'sent_at', 'opened_at')
    search_fields = ('contact__email', 'contact__first_name', 'contact__last_name')
    readonly_fields = ('sent_at', 'opened_at', 'clicked_at', 'unsubscribed_at')
    date_hierarchy = 'sent_at'

    fieldsets = (
        ('Recipient Information', {
            'fields': ('campaign', 'contact', 'status')
        }),
        ('Tracking', {
            'fields': ('sent_at', 'opened_at', 'clicked_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AutomationWorkflow)
class AutomationWorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Workflow Information', {
            'fields': ('name', 'description', 'status')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new workflow
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class AutomationStepInline(admin.TabularInline):
    model = AutomationStep
    extra = 1
    fields = ('name', 'trigger_type', 'action_type', 'email_template', 'delay', 'order')

@admin.register(AutomationStep)
class AutomationStepAdmin(admin.ModelAdmin):
    list_display = ('name', 'workflow', 'trigger_type', 'action_type', 'order')
    list_filter = ('trigger_type', 'action_type', 'workflow')
    search_fields = ('name', 'workflow__name')
    ordering = ('workflow', 'order')

    fieldsets = (
        ('Step Information', {
            'fields': ('workflow', 'name', 'trigger_type', 'action_type')
        }),
        ('Configuration', {
            'fields': ('email_template', 'delay', 'order')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(workflow__created_by=request.user)
