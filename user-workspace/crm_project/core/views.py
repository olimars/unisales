from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .models import UserProfile, CompanySettings, Notification, AuditLog, CustomField
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    CompanySettingsSerializer,
    NotificationSerializer,
    AuditLogSerializer,
    CustomFieldSerializer,
    ChangePasswordSerializer,
    UserPreferencesSerializer,
    NotificationPreferencesSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        Get or update the current user's information.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """
        Change user password.
        """
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data['old_password']):
                return Response(
                    {'error': 'Wrong password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'status': 'password changed'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put'])
    def preferences(self, request, pk=None):
        """
        Get or update user preferences.
        """
        user = self.get_object()
        if request.method == 'GET':
            serializer = UserPreferencesSerializer(user.profile)
            return Response(serializer.data)
        
        serializer = UserPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(user.profile, key, value)
            user.profile.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanySettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing company settings.
    """
    queryset = CompanySettings.objects.all()
    serializer_class = CompanySettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        """
        Get or create company settings.
        """
        try:
            return CompanySettings.objects.first()
        except CompanySettings.DoesNotExist:
            return CompanySettings.objects.create()

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Mark all notifications as read.
        """
        self.get_queryset().update(is_read=True)
        return Response({'status': 'notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark a specific notification as read.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing audit logs.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

class CustomFieldViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing custom fields.
    """
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model_name', 'field_type']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def model_fields(self, request):
        """
        Get custom fields for a specific model.
        """
        model_name = request.query_params.get('model')
        if not model_name:
            return Response(
                {'error': 'model parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        fields = self.get_queryset().filter(model_name=model_name)
        serializer = self.get_serializer(fields, many=True)
        return Response(serializer.data)

class NotificationPreferencesView(generics.RetrieveUpdateAPIView):
    """
    View for managing notification preferences.
    """
    serializer_class = NotificationPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        return Response(profile.notification_preferences)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile.notification_preferences = serializer.validated_data
        profile.save()
        return Response(profile.notification_preferences)
