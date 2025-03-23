from django.contrib import admin
from .models import Dashboard, Widget, Report, ReportExport, Metric

class WidgetInline(admin.TabularInline):
    model = Widget
    extra = 0
    fields = ('name', 'widget_type', 'position_x', 'position_y', 'width', 'height')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'is_public', 'widget_count', 'created_at')
    list_filter = ('is_public', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WidgetInline]
    date_hierarchy = 'created_at'

    def widget_count(self, obj):
        return obj.widgets.count()
    widget_count.short_description = 'Widgets'

    fieldsets = (
        ('Dashboard Information', {
            'fields': ('name', 'description', 'is_public')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new dashboard
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'dashboard', 'widget_type', 'refresh_interval', 'created_at')
    list_filter = ('widget_type', 'created_at', 'dashboard')
    search_fields = ('name', 'query')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Widget Information', {
            'fields': ('dashboard', 'name', 'widget_type')
        }),
        ('Query Configuration', {
            'fields': ('query', 'refresh_interval')
        }),
        ('Layout', {
            'fields': ('position_x', 'position_y', 'width', 'height')
        }),
        ('Additional Configuration', {
            'fields': ('configuration',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ReportExportInline(admin.TabularInline):
    model = ReportExport
    extra = 0
    fields = ('format', 'file', 'created_by', 'created_at')
    readonly_fields = ('created_by', 'created_at')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'is_scheduled', 'schedule_type', 'created_by', 'last_run')
    list_filter = ('report_type', 'is_scheduled', 'schedule_type', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'last_run')
    filter_horizontal = ('recipients',)
    inlines = [ReportExportInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Report Information', {
            'fields': ('name', 'description', 'report_type')
        }),
        ('Query Configuration', {
            'fields': ('query', 'parameters')
        }),
        ('Schedule', {
            'fields': ('is_scheduled', 'schedule_type', 'recipients')
        }),
        ('Execution Information', {
            'fields': ('last_run',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new report
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ReportExport)
class ReportExportAdmin(admin.ModelAdmin):
    list_display = ('report', 'format', 'created_by', 'created_at')
    list_filter = ('format', 'created_at')
    search_fields = ('report__name',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Export Information', {
            'fields': ('report', 'format', 'file')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new export
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'object_id', 'value', 'timestamp')
    list_filter = ('content_type', 'timestamp')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Metric Information', {
            'fields': ('name', 'description')
        }),
        ('Target Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Value', {
            'fields': ('value', 'timestamp')
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
