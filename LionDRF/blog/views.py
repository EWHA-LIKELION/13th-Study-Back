from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PostList(views.APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    keyword = request.GET.get('keyword')
    if keyword:
      post = Post.objects.filter(user=request.user, title__icontains=keyword)
    else:
      post = Post.objects.filter(user=request.user)
    serializer = PostSerializer(post, many=True)
    return Response({
      "count": post.count(),
      "results": serializer.data
    })
  
  def post(self, request, format=None):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(views.APIView):
  permission_classes = [IsAuthenticated]
  
  def get_object(self, pk):
    try:
      return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
      raise Http404
        
  def get(self, request, pk, format=None):
    post = self.get_object(pk)
    if post.user != request.user:
      return Response({"message": "조회가 불가능합니다. (자신이 쓴 글만 조회 가능)"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post)
    liked = LikePost.objects.filter(user=request.user, post=post).exists()
    response_data = dict(serializer.data)
    response_data['liked'] = liked    
    return Response(response_data)
  
  def put(self, request, pk, format=None):
    post = self.get_object(pk)
    if post.user != request.user:
      return Response({"message": "수정이 불가능합니다. (자신이 쓴 글만 수정 가능)"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, pk, format=None):
    post=get_object_or_404(Post, pk=pk)
    if post.user != request.user:
      return Response({"message": "삭제가 불가능합니다. (자신이 쓴 글만 삭제 가능)"}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response({"message":"게시물 삭제 성공"})
  

class LikePostView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, post_id):
    post = get_object_or_404(Post, id=post_id)
    _, created = LikePost.objects.get_or_create(post=post, user=request.user)
    if not created:
      return Response({"message": "이미 좋아요를 누르셨습니다."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "좋아요 완료"}, status=status.HTTP_201_CREATED)
  

class CommentView(views.APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer=CommentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data)
    return Response(serializer.errors)
  

class CommentDetail(views.APIView):
  permission_classes = [IsAuthenticated]
  def get_object(self, pk):
    return get_object_or_404(Comment, pk=pk)

  def get(self, request, pk, format=None):
    comment = self.get_object(pk)
    if comment.user != request.user:
      return Response({"message": "조회가 불가능합니다. (자신이 쓴 댓글만 조회 가능)"}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    comment = self.get_object(pk)
    if comment.user != request.user:
      return Response({"message": "수정이 불가능합니다. (자신이 쓴 댓글만 수정 가능)"}, status=status.HTTP_403_FORBIDDEN)
    serializer=CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    comment=get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
      return Response({"message": "삭제가 불가능합니다. (자신이 쓴 댓글만 삭제 가능)"}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({"message":"댓글 삭제 성공"})
  
class LikeCommentView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    _, created = LikeComment.objects.get_or_create(comment=comment, user=request.user)
    if not created:
      return Response({"message": "이미 좋아요를 누르셨습니다."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "좋아요 완료"}, status=status.HTTP_201_CREATED)