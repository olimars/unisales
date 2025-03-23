from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet)
router.register(r'interactions', views.InteractionViewSet)

app_name = 'contacts'

urlpatterns = [
    path('', include(router.urls)),
]