from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'ticket-categories', views.TicketCategoryViewSet)
router.register(r'kb-categories', views.KnowledgeBaseCategoryViewSet)
router.register(r'articles', views.ArticleViewSet)

app_name = 'support'

urlpatterns = [
    path('', include(router.urls)),
]