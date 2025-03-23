from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'company-settings', views.CompanySettingsViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'audit-logs', views.AuditLogViewSet)
router.register(r'custom-fields', views.CustomFieldViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'notification-preferences/',
        views.NotificationPreferencesView.as_view(),
        name='notification-preferences'
    ),
]