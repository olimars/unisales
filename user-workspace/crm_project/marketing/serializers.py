from rest_framework import serializers
from django.contrib.auth.models import User
from contacts.serializers import ContactSerializer, UserSerializer
from contacts.models import Contact
from .models import Campaign, EmailTemplate, CampaignRecipient, AutomationWorkflow, AutomationStep

class EmailTemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class CampaignRecipientSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact',
        write_only=True
    )

    class Meta:
        model = CampaignRecipient
        fields = [
            'id', 'campaign', 'contact', 'contact_id',
            'status', 'sent_at', 'opened_at', 'clicked_at',
            'unsubscribed_at'
        ]
        read_only_fields = [
            'sent_at', 'opened_at', 'clicked_at',
            'unsubscribed_at'
        ]

class CampaignSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    recipients = CampaignRecipientSerializer(many=True, read_only=True)
    recipient_count = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'type',
            'status', 'start_date', 'end_date',
            'budget', 'created_by', 'recipients',
            'recipient_count', 'success_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def get_recipient_count(self, obj):
        return obj.recipients.count()

    def get_success_rate(self, obj):
        total = obj.recipients.count()
        if total == 0:
            return 0
        successful = obj.recipients.filter(status__in=['opened', 'clicked']).count()
        return round((successful / total) * 100, 2)

class CampaignListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    created_by = UserSerializer(read_only=True)
    recipient_count = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'type', 'status',
            'start_date', 'end_date', 'created_by',
            'recipient_count', 'created_at'
        ]

    def get_recipient_count(self, obj):
        return obj.recipients.count()

class AutomationStepSerializer(serializers.ModelSerializer):
    email_template = EmailTemplateSerializer(read_only=True)
    email_template_id = serializers.PrimaryKeyRelatedField(
        queryset=EmailTemplate.objects.all(),
        source='email_template',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = AutomationStep
        fields = [
            'id', 'workflow', 'name', 'trigger_type',
            'action_type', 'email_template', 'email_template_id',
            'delay', 'order'
        ]

    def validate(self, data):
        """
        Validate that email template is provided when action type is send_email
        """
        if data.get('action_type') == 'send_email' and not data.get('email_template'):
            raise serializers.ValidationError(
                "Email template is required when action type is 'send_email'"
            )
        return data

class AutomationWorkflowSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    steps = AutomationStepSerializer(many=True, read_only=True)

    class Meta:
        model = AutomationWorkflow
        fields = [
            'id', 'name', 'description', 'status',
            'created_by', 'steps', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        steps_data = self.context.get('steps', [])
        workflow = AutomationWorkflow.objects.create(**validated_data)
        
        for step_data in steps_data:
            step_data['workflow'] = workflow
            AutomationStep.objects.create(**step_data)
        
        return workflow

class AutomationWorkflowListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    created_by = UserSerializer(read_only=True)
    step_count = serializers.SerializerMethodField()

    class Meta:
        model = AutomationWorkflow
        fields = [
            'id', 'name', 'status', 'created_by',
            'step_count', 'created_at'
        ]

    def get_step_count(self, obj):
        return obj.steps.count()