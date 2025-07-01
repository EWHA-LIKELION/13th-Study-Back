from rest_framework import serializers
from blog.models import Post, LANGUAGE_CHOICES, Comment
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id', 'post', 'username', 'comment_text', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments=CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model=Post
        fields=['id', 'user', 'title', 'date', 'body', 'language', 'likes', 'comments']

    
