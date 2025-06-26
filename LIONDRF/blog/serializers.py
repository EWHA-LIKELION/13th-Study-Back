from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields= ['id','post', 'username','comment_text','created_at']


class PostSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True, read_only=True) #many=True는 1:N의 관계! 역참조이다!!
    class Meta:
        model = Post
        fields = ['id', 'title', 'date', 'body', 'language', 'comments']


class AnswerSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id', 'question', 'username', 'answer_text', 'created_at', 'likes_count', 'is_liked']

    def create(self, validated_data):
        user = self.context['request'].user  # access token에서 유저 추출
        return Answer.objects.create(user=user, **validated_data)
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False


class QuestionSerializer(serializers.ModelSerializer):
    answers=AnswerSerializer(many=True, read_only=True) #many=True는 1:N의 관계! 역참조이다!!
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'date', 'body', 'language', 'answers', 'likes_count', 'is_liked']

    def create(self, validated_data):
        user = self.context['request'].user  # access token 기반 인증된 유저
        return Question.objects.create(user=user, **validated_data)
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False



