from rest_framework import serializers
from django.contrib.auth.models import User
from contacts.serializers import ContactSerializer, UserSerializer
from contacts.models import Contact
from .models import (
    TicketCategory,
    Ticket,
    TicketComment,
    KnowledgeBaseCategory,
    Article,
    ArticleAttachment
)

class TicketCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = TicketCategory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_subcategories(self, obj):
        return TicketCategorySerializer(obj.subcategories.all(), many=True).data

class TicketCommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = TicketComment
        fields = '__all__'
        read_only_fields = ['created_at']

class TicketSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact',
        write_only=True
    )
    category = TicketCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'contact', 'contact_id',
            'category', 'category_id', 'priority', 'status',
            'source', 'assigned_to', 'assigned_to_id',
            'created_by', 'comments', 'created_at',
            'updated_at', 'resolved_at', 'due_date'
        ]
        read_only_fields = ['created_at', 'updated_at', 'resolved_at']

    def validate_due_date(self, value):
        """
        Check that due date is not in the past.
        """
        from django.utils import timezone
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

class TicketListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    contact = serializers.SerializerMethodField()
    assigned_to = UserSerializer(read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'contact', 'category',
            'priority', 'status', 'assigned_to',
            'created_at', 'due_date'
        ]

    def get_contact(self, obj):
        return {
            'id': obj.contact.id,
            'name': f"{obj.contact.first_name} {obj.contact.last_name}",
            'email': obj.contact.email
        }

    def get_category(self, obj):
        if obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name
            }
        return None

class KnowledgeBaseCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeBaseCategory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_subcategories(self, obj):
        return KnowledgeBaseCategorySerializer(obj.subcategories.all(), many=True).data

    def get_article_count(self, obj):
        return obj.articles.filter(is_published=True).count()

class ArticleAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAttachment
        fields = '__all__'
        read_only_fields = ['created_at']

class ArticleSerializer(serializers.ModelSerializer):
    category = KnowledgeBaseCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=KnowledgeBaseCategory.objects.all(),
        source='category',
        write_only=True
    )
    created_by = UserSerializer(read_only=True)
    attachments = ArticleAttachmentSerializer(many=True, read_only=True)
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'category', 'category_id',
            'tags', 'tags_list', 'is_published', 'view_count',
            'helpful_count', 'not_helpful_count', 'created_by',
            'attachments', 'created_at', 'updated_at',
            'published_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'published_at',
            'view_count', 'helpful_count', 'not_helpful_count'
        ]

    def get_tags_list(self, obj):
        return [tag.strip() for tag in obj.tags.split(',') if tag.strip()] if obj.tags else []

class ArticleListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    category = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'category', 'tags_list',
            'is_published', 'view_count', 'created_by',
            'created_at', 'published_at'
        ]

    def get_category(self, obj):
        if obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name
            }
        return None

    def get_tags_list(self, obj):
        return [tag.strip() for tag in obj.tags.split(',') if tag.strip()] if obj.tags else []