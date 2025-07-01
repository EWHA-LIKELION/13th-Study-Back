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
        serializer=PostSerializer(post, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer=PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        post=self.get_object(pk)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post=get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"message":"게시물 삭제 성공"})
    

class PostListLang(views.APIView):
     def get(self, request, format=None):
        lang=request.query_params.get('language')
        if lang:
            post=Post.objects.filter(language=lang)
        else:
            post=Post.objects.all()
        serializer=PostSerializer(post, many=True)
        return Response(serializer.data)
     

class Comment(views.APIView):
    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
