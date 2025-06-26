from rest_framework import serializers
from .models import Post, Answer, LANGUAGE_CHOICES, Comment
        
class AnswerSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)  # 추가
    class Meta:
        model = Answer
        fields = ['id', 'title', 'post_id', 'date', 'body', 'language']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        post_id = validated_data.pop('post_id')
        post = Post.objects.get(id=post_id)
        return Answer.objects.create(post=post, **validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'username', 'comment_text', 'created_at']
        
class PostSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'date', 'body', 'language', 'comments']
        
    def create(self, validated_data): # user 정보를 포함하여 Post 객체 생성
        validated_data['user'] = self.context['request'].user
        return Post.objects.create(**validated_data)    