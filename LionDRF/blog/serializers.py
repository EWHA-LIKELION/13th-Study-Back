from rest_framework import serializers
from blog.models import Post, LANGUAGE_CHOICES

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'date', 'body', 'language']