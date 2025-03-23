from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'integrations', views.IntegrationViewSet)
router.register(r'webhooks', views.WebhookViewSet)
router.register(r'data-mappings', views.DataMappingViewSet)
router.register(r'sync-logs', views.SyncLogViewSet)
router.register(r'external-references', views.ExternalReferenceViewSet)

app_name = 'integrations'

urlpatterns = [
    path('', include(router.urls)),
]