from rest_framework import serializers
from .models import Post, Community, Question, Answer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id','writer','created_at','hashtag',)
        depth = 1

class CommunitySerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Community

class QuestionSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id','writer','created_at','question',)
        depth = 1