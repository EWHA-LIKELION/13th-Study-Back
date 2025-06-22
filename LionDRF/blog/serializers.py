from rest_framework import serializers
from blog.models import Post, Comment, LANGUAGE_CHOICES

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['id', 'post', 'comment_text', 'created_at']


class PostSerializer(serializers.ModelSerializer):
  comments=CommentSerializer(many=True, read_only=True)
  
  class Meta:
    model = Post
    fields = ['id', 'title', 'date', 'body', 'language', 'comments']