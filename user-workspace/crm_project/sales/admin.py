from django.contrib import admin
from .models import Pipeline, Stage, Opportunity, Activity

@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    fieldsets = (
        ('Pipeline Information', {
            'fields': ('name', 'description')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'pipeline', 'order', 'probability')
    list_filter = ('pipeline',)
    search_fields = ('name',)
    ordering = ('pipeline', 'order')

    fieldsets = (
        ('Stage Information', {
            'fields': ('pipeline', 'name', 'order', 'probability')
        }),
    )

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact', 'stage', 'amount', 'priority', 'expected_close_date', 'assigned_to')
    list_filter = ('stage', 'priority', 'assigned_to', 'created_at')
    search_fields = ('title', 'contact__first_name', 'contact__last_name', 'contact__company')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'contact', 'stage')
        }),
        ('Details', {
            'fields': ('amount', 'priority', 'expected_close_date', 'assigned_to')
        }),
        ('Additional Information', {
            'fields': ('description',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_to=request.user)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('subject', 'opportunity', 'type', 'due_date', 'completed', 'assigned_to')
    list_filter = ('type', 'completed', 'due_date', 'assigned_to')
    search_fields = ('subject', 'notes', 'opportunity__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('due_date',)
    date_hierarchy = 'due_date'

    fieldsets = (
        ('Activity Information', {
            'fields': ('opportunity', 'type', 'subject', 'due_date')
        }),
        ('Status', {
            'fields': ('completed', 'assigned_to')
        }),
        ('Details', {
            'fields': ('notes',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            assigned_to=request.user
        )
