from rest_framework import serializers
from django.contrib.auth.models import User
from contacts.serializers import ContactSerializer, UserSerializer
from .models import Pipeline, Stage, Opportunity, Activity

class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

    def validate_order(self, value):
        """
        Check that the order is unique within the pipeline.
        """
        pipeline_id = self.initial_data.get('pipeline')
        if Stage.objects.filter(pipeline_id=pipeline_id, order=value).exists():
            if self.instance and self.instance.order == value:
                return value
            raise serializers.ValidationError("A stage with this order already exists in the pipeline.")
        return value

class OpportunitySerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact',
        write_only=True
    )
    stage = StageSerializer(read_only=True)
    stage_id = serializers.PrimaryKeyRelatedField(
        queryset=Stage.objects.all(),
        source='stage',
        write_only=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'contact', 'contact_id', 
            'stage', 'stage_id', 'amount', 'priority',
            'expected_close_date', 'assigned_to', 'assigned_to_id',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class OpportunityListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    contact = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'contact', 'stage',
            'amount', 'priority', 'expected_close_date',
            'assigned_to', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_contact(self, obj):
        return {
            'id': obj.contact.id,
            'name': f"{obj.contact.first_name} {obj.contact.last_name}",
            'company': obj.contact.company
        }

    def get_stage(self, obj):
        return {
            'id': obj.stage.id,
            'name': obj.stage.name,
            'probability': obj.stage.probability
        }

class ActivitySerializer(serializers.ModelSerializer):
    opportunity = OpportunityListSerializer(read_only=True)
    opportunity_id = serializers.PrimaryKeyRelatedField(
        queryset=Opportunity.objects.all(),
        source='opportunity',
        write_only=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Activity
        fields = [
            'id', 'opportunity', 'opportunity_id',
            'type', 'subject', 'due_date', 'completed',
            'notes', 'assigned_to', 'assigned_to_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_due_date(self, value):
        """
        Check that due date is not in the past.
        """
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value