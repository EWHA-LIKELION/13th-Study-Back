from django.shortcuts import render
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

    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        post=Post.objects.all()
        serializer=PostSerializer(post, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer=PostSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(user=request.user) #작성자 자동 저장 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PostDetail(views.APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        post=self.get_object(pk)
        serializer=PostSerializer(post, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        post=self.get_object(pk)
        #작성자만 수정 가능하도록 함
        if post.user!=request.user:
            return Response({"message":"수정 권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)

        serializer=PostSerializer(post, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post=get_object_or_404(Post, pk=pk)
        if post.user!=request.user:
            return Response({"message":"삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message":"게시물 삭제 성공"})
    

class PostListLang(views.APIView):
     def get(self, request, format=None):
        lang=request.query_params.get('language')
        if lang:
            post=Post.objects.filter(language=lang)
        else:
            post=Post.objects.all()
        serializer=PostSerializer(post, context={'request':request})
        return Response(serializer.data)
     

class Comment(views.APIView):
    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) #작성자 자동 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentView(views.APIView):
    def get(self, request, pk, format=None):
        comment=get_object_or_404(Comment, pk=pk)
        serializer=CommentSerializer(comment, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        comment=get_object_or_404(Comment, pk=pk)
        if comment.user!=request.user:
            return Response({"message":"수정 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer=CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk, format=None):
        comment=get_object_or_404(Comment, pk=pk)
        if comment.user!=request.user:
            return Response({"message":"삭제 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({"messsage":"댓글 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)

class LikePostView(views.APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        post=get_object_or_404(Post, pk=pk)
        user=request.user

        like, created=LikePost.objects.get_or_create(user=user, post=post)

        if not created: #이미 좋아요가 존재하면 삭제
            like.delete()
            return Response({"message":"좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"좋아요 추가"}, status=status.HTTP_201_CREATED)
        

class LikeCommentView(views.APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        comment=get_object_or_404(Comment, pk=pk)
        user=request.user

        like, created=LikeComment.objects.get_or_create(user=user, comment=comment)

        if not created:
            like.delete() #이미 좋아요 한 경우 취소 
            return Response({"message":"댓글 좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"댓글 좋아요 추가"}, status=status.HTTP_201_CREATED)
        