from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404


# Create your views here.
class PostList(views.APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        
            # 🔍 내가 쓴 글만 보기
        mine = request.query_params.get('mine')
        if mine == 'true':
            queryset = queryset.filter(user=request.user)
        
        keyword = request.query_params.get('keyword') # 검색 쿼리
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(body__icontains=keyword)
            )
            
        ordering = request.query_params.get('ordering') # 정렬 쿼리
        if ordering:
            queryset = queryset.order_by(ordering)
            
        serializer = PostSerializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'posts': serializer.data
        }) 
        
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, )
        if serializer.is_valid():
            serializer.save()  # user 정보를 포함하여 Post 객체 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetail(views.APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None): # UPDATE
        post = self.get_object(pk)
        serializer= PostSerializer(post, data=request.data, context={'request': request})
        if request.user != post.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=403)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user != post.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=403)

        post.delete()
        return Response({"message": "게시물 삭제 성공"})
    
    
# answer


class AnswerList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Answer.objects.all()

        # 검색 필터
        keyword = request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(body__icontains=keyword)
            )

        # 정렬
        ordering = request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = AnswerSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'answers': serializer.data
        })

    def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetail(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        answer = self.get_object(pk)
        if request.user != answer.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=403)

        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        answer = get_object_or_404(Answer, pk=pk)
        if request.user != answer.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=403)

        answer.delete()
        return Response({"message": "게시물 삭제 성공"})

class AllList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        answers = Answer.objects.all()

        post_serializer = PostSerializer(posts, many=True)
        answer_serializer = AnswerSerializer(answers, many=True)

        return Response({
            'posts': post_serializer.data,
            'answers': answer_serializer.data
        })
        
class Comment(views.APIView):
    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)