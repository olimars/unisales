from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, CompanySettings, Notification, AuditLog, CustomField

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'role', 'phone', 'department',
            'profile_picture', 'theme_preference',
            'notification_preferences', 'dashboard_layout',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'full_name', 'is_active',
            'is_staff', 'profile', 'date_joined',
            'last_login'
        ]
        read_only_fields = ['date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
            
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
            
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        
        if profile_data and instance.profile:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
            
        return instance

class CompanySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySettings
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at']

class AuditLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['timestamp']

class CustomFieldSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomField
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Validate that options are provided for select/multiselect fields
        """
        if data.get('field_type') in ['select', 'multiselect']:
            if not data.get('options'):
                raise serializers.ValidationError(
                    "Options are required for select/multiselect fields"
                )
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                "New password and confirm password do not match"
            )
        return data

class UserPreferencesSerializer(serializers.Serializer):
    theme = serializers.ChoiceField(
        choices=UserProfile.THEME_CHOICES,
        required=False
    )
    notification_preferences = serializers.JSONField(required=False)
    dashboard_layout = serializers.JSONField(required=False)

class NotificationPreferencesSerializer(serializers.Serializer):
    email_notifications = serializers.BooleanField(required=False)
    push_notifications = serializers.BooleanField(required=False)
    notification_types = serializers.MultipleChoiceField(
        choices=[
            'task_assignments',
            'mentions',
            'due_dates',
            'status_changes',
            'comments'
        ],
        required=False
    )