from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404

# Create your views here.
class PostList(views.APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        keyword= request.GET.get('keyword', None) #keyword 검색
        if keyword:
            post=Post.objects.filter(title__icontains=keyword)
        else:
            post = Post.objects.filter(author=request.user) #현재 로그인 유저의 글만 조회
            #post=Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response({
            'count': post.count(),
            'results': serializer.data
        })


    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user) #현재 로그인 유저 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            post = Post.objects.get(pk=pk)
            if post.author != user:
                return None #작성자가 아닌 유저가 요청했을 때 None 반환
            return post
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        post = self.get_object(pk, request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"message":"삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message":"게시물 삭제 성공"})
    
class CommentView(views.APIView):
    def get(self, request, format=None):
        post = Comment.objects.filter(author=request.user)
        serializer = CommentSerializer(post, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user) 
            return Response(serializer.data)
        return Response(serializer.errors)
    
class CommentDetail(views.APIView):
    def get_object(self, pk, user):
        try:
            post=Comment.objects.get(pk=pk)
            if post.author != user:
                return None #작성자가 아닌 유저가 요청했을 때 None 반환
        except Comment.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"message": "댓글 수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post=get_object_or_404(Comment, pk=pk)
        if post.author != request.user:
            return Response({"message":"댓글 삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message":"댓글 삭제 성공"})
    
class PostLike(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        
        post.likes.add(request.user)
        return Response({"message": "좋아요"})
    
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        
        if request.user in post.likes.all():
            return Response(True)
        else:
            return Response(False)
        
class CommentLike(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = get_object_or_404(Comment, pk=pk)
        
        post.likes.add(request.user)
        return Response({"message": "좋아요"})