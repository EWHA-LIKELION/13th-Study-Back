from rest_framework import serializers
from accounts.models import User
from .models import Post, Community, Question, Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','image',)

class AnswerSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id','created_at','question',)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id','created_at','hashtag',)

class CommunitySerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Community

class QuestionSerializer(PostSerializer):
    writer = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta(PostSerializer.Meta):
        model = Question