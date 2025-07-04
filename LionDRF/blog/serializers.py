from rest_framework import serializers
from blog.models import Post, LANGUAGE_CHOICES, Comment, LikePost, LikeComment
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class CommentSerializer(serializers.ModelSerializer):
    liked=serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields=['id', 'post', 'comment_text', 'created_at', 'liked'] #user 필드 삭제 

    def get_liked(self, obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            return LikeComment.objects.filter(comment=obj, user=request.user).exists()
        return False

class PostSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments=CommentSerializer(many=True, read_only=True)
    liked=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=['id', 'user', 'title', 'date', 'body', 'language', 'likes', 'comments', 'liked'] #user 필드 삭제 
        read_only_fields=['likes']

    def get_liked(self, obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            return LikePost.objects.filter(post=obj, user=request.user).exists()
        return False

   
  