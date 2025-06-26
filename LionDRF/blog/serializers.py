from rest_framework import serializers
from blog.models import Post, Comment, LANGUAGE_CHOICES

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    

    class Meta:
        model = Comment
        fields = ['id','post','author','comment_text','created_at']
        # fields = ['id','post','username','comment_text','created_at']

class PostSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True, read_only=True) #1:N관계
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'date', 'author', 'body', 'language', 'comments']

