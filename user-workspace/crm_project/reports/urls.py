from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet)
router.register(r'widgets', views.WidgetViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'metrics', views.MetricViewSet)

app_name = 'reports'

urlpatterns = [
    path('', include(router.urls)),
]