from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, CompanySettings, Notification, AuditLog, CustomField

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Personal Information', {
            'fields': ('role', 'phone', 'department', 'profile_picture')
        }),
        ('Preferences', {
            'fields': ('theme_preference', 'notification_preferences')
        }),
        ('Layout Settings', {
            'fields': ('dashboard_layout',),
            'classes': ('collapse',)
        }),
    )

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'get_role', 'date_joined'
    )
    list_filter = BaseUserAdmin.list_filter + ('profile__role',)
    
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except UserProfile.DoesNotExist:
            return '-'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone', 'time_zone', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'logo', 'address', 'phone', 'email', 'website')
        }),
        ('Regional Settings', {
            'fields': ('time_zone', 'date_format', 'time_format', 'currency')
        }),
        ('Fiscal Settings', {
            'fields': ('fiscal_year_start',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one company settings instance
        if CompanySettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of company settings
        return False

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read', 'link')
        }),
        ('System Fields', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'record_id', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'model_name', 'record_id')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Action Details', {
            'fields': ('user', 'action', 'model_name', 'record_id')
        }),
        ('Changes', {
            'fields': ('changes',)
        }),
        ('Request Information', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('System Fields', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent manual creation of audit logs
        return False

    def has_change_permission(self, request, obj=None):
        # Prevent modification of audit logs
        return False

@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'field_type', 'is_required', 'created_by')
    list_filter = ('model_name', 'field_type', 'is_required', 'created_at')
    search_fields = ('name', 'model_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Field Information', {
            'fields': ('name', 'model_name', 'field_type', 'is_required')
        }),
        ('Field Configuration', {
            'fields': ('options', 'default_value')
        }),
        ('System Fields', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new custom field
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
