from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pipelines', views.PipelineViewSet)
router.register(r'stages', views.StageViewSet)
router.register(r'opportunities', views.OpportunityViewSet)
router.register(r'activities', views.ActivityViewSet)

app_name = 'sales'

urlpatterns = [
    path('', include(router.urls)),
]