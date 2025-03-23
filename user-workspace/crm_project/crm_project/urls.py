from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('core.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/support/', include('support.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/integrations/', include('integrations.urls')),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
