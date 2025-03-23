from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, Interaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class InteractionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ['created_at']

class ContactSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'company', 'position', 'status', 'notes',
            'assigned_to', 'assigned_to_id', 'interactions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_email(self, value):
        """
        Check that the email is unique (case-insensitive).
        """
        if Contact.objects.filter(email__iexact=value).exists():
            if self.instance and self.instance.email.lower() == value.lower():
                return value
            raise serializers.ValidationError("A contact with this email already exists.")
        return value

class ContactListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'company', 'status', 'assigned_to', 'created_at'
        ]
        read_only_fields = ['created_at']