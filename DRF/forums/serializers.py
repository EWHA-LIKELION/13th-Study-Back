from rest_framework import serializers
from accounts.models import User
from .models import Post, Community, Question, Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','image',)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id','created_at','hashtag',)
        depth = 1

class CommunitySerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Community

class QuestionSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Question
        read_only_fields = PostSerializer.Meta.read_only_fields + ('writer',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id','created_at','writer','question',)
        depth = 1