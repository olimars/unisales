from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'campaigns', views.CampaignViewSet)
router.register(r'email-templates', views.EmailTemplateViewSet)
router.register(r'automation-workflows', views.AutomationWorkflowViewSet)
router.register(r'automation-steps', views.AutomationStepViewSet)

app_name = 'marketing'

urlpatterns = [
    path('', include(router.urls)),
]