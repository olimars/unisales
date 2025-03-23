from django.contrib import admin
from .models import Integration, Webhook, SyncLog, DataMapping, ExternalReference

class WebhookInline(admin.TabularInline):
    model = Webhook
    extra = 0
    fields = ('event_type', 'url', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

class DataMappingInline(admin.TabularInline):
    model = DataMapping
    extra = 0
    fields = ('source_model', 'target_model', 'mapping_type', 'source_field', 'target_field')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'integration_type', 'provider', 'status', 'created_by', 'last_sync')
    list_filter = ('integration_type', 'provider', 'status', 'created_at')
    search_fields = ('name', 'provider')
    readonly_fields = ('created_at', 'updated_at', 'last_sync', 'created_by')
    inlines = [WebhookInline, DataMappingInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Integration Information', {
            'fields': ('name', 'integration_type', 'provider', 'status')
        }),
        ('Configuration', {
            'fields': ('configuration', 'webhook_url', 'api_key')
        }),
        ('Credentials', {
            'fields': ('credentials',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'last_sync', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new integration
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('integration', 'event_type', 'url', 'is_active', 'created_at')
    list_filter = ('event_type', 'is_active', 'created_at')
    search_fields = ('url', 'integration__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Webhook Information', {
            'fields': ('integration', 'event_type', 'url', 'is_active')
        }),
        ('Security', {
            'fields': ('secret_key',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = (
        'integration', 'status', 'start_time', 'end_time',
        'records_processed', 'records_succeeded', 'records_failed'
    )
    list_filter = ('status', 'start_time', 'integration')
    search_fields = ('integration__name', 'error_message')
    readonly_fields = ('start_time', 'end_time')
    date_hierarchy = 'start_time'

    fieldsets = (
        ('Sync Information', {
            'fields': ('integration', 'status', 'start_time', 'end_time')
        }),
        ('Results', {
            'fields': ('records_processed', 'records_succeeded', 'records_failed')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Additional Data', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
    )

@admin.register(DataMapping)
class DataMappingAdmin(admin.ModelAdmin):
    list_display = (
        'integration', 'source_model', 'target_model',
        'mapping_type', 'source_field', 'target_field'
    )
    list_filter = ('mapping_type', 'integration', 'source_model', 'target_model')
    search_fields = ('source_field', 'target_field', 'integration__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Mapping Information', {
            'fields': ('integration', 'source_model', 'target_model')
        }),
        ('Field Mapping', {
            'fields': ('mapping_type', 'source_field', 'target_field', 'is_required')
        }),
        ('Transformation', {
            'fields': ('transformation_rule',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ExternalReference)
class ExternalReferenceAdmin(admin.ModelAdmin):
    list_display = ('integration', 'content_type', 'object_id', 'external_id', 'last_synced')
    list_filter = ('integration', 'content_type', 'last_synced')
    search_fields = ('external_id', 'external_url')
    readonly_fields = ('last_synced',)
    date_hierarchy = 'last_synced'

    fieldsets = (
        ('Reference Information', {
            'fields': ('integration', 'content_type', 'object_id')
        }),
        ('External Data', {
            'fields': ('external_id', 'external_url')
        }),
        ('Sync Information', {
            'fields': ('last_synced',)
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
