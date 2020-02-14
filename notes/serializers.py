from rest_framework import serializers
from .models import Note, Category


class NoteSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(
        source='category.title', read_only=True)
    creator_username = serializers.CharField(
        source='category.title', read_only=True)    
    class Meta:
        model = Note
        fields = ['uuid', 'title', 'context', 'category', 'category_title', 'creator',
                  'creator_username', 'bookmark', 'published', 'dtcreate', 'dtupdate']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
