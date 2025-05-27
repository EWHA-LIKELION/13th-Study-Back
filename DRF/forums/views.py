from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from .models import Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer
from .serializers import CommunitySerializer, QuestionSerializer, AnswerSerializer

def add_hashtag(instance):
    hashtags = [word for word in instance.content.split() if word.startswith('#')]
    for hashtag in hashtags:
        (obj, created) = Hashtag.objects.get_or_create(hashtag=hashtag)
        instance.hashtag.add(obj)

class CommunityRoot(views.APIView):
    def get(self, request, format=None):
        # 커뮤니티 게시물 목록 조회

        query_string_search = request.query_params.get('search')

        condition = Q()
        if query_string_search:
            condition &= Q(title__contains=query_string_search) | Q(content__contains=query_string_search)
        communities = Community.objects.filter(condition).order_by('-created_at')

        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # 커뮤니티 게시물 추가

        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                created_at=timezone.now(),
            )
            add_hashtag(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommunityPk(views.APIView):
    def get(self, request, pk, format=None):
        # 커뮤니티 게시물 상세 조회

        community = get_object_or_404(Community, pk=pk)
        serializer = CommunitySerializer(community)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        # 커뮤니티 게시물 수정

        community = get_object_or_404(Community, pk=pk)
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.hashtag.clear()
            add_hashtag(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # 커뮤니티 게시물 삭제

        community = get_object_or_404(Community, pk=pk)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class QuestionRoot(views.APIView):
    def get(self, request, format=None):
        # 질문 게시물 목록 조회

        query_string_search = request.query_params.get('search')
        query_string_status = request.query_params.get('status')
        question_status = {
            '도와주세요': False,
            '해결됐어요': True,
        }.get(query_string_status)

        condition = Q()
        if query_string_search:
            condition &= Q(title__contains=query_string_search) | Q(content__contains=query_string_search)
        if question_status:
            condition &= Q(status=question_status)
        questions = Question.objects.filter(condition).order_by('-created_at')

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # 질문 게시물 추가

        user = get_object_or_404(User, pk=1) # JWT 배우기 전까지 임시로 1 할당
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                created_at=timezone.now(),
                writer=user,
            )
            add_hashtag(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionPk(views.APIView):
    def get(self, request, pk, format=None):
        # 질문 게시글 상세 조회

        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        # 질문 게시글 수정

        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.hashtag.clear()
            add_hashtag(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # 질문 게시글 삭제

        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnswerRoot(views.APIView):
    def post(self, request, format=None):
        # 답변 게시글 추가

        user = get_object_or_404(User, pk=1) # JWT 배우기 전까지 임시로 1 할당

        query_string_question_id = request.query_params.get('question_id')
        question = get_object_or_404(Question, pk=query_string_question_id)
        
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_at=timezone.now(),
                writer=user,
                question=question,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerPk(views.APIView):
    def put(self, request, pk, format=None):
        # 답변 게시글 수정

        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # 답변 게시글 삭제

        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LikeQuestionRoot(views.APIView):
    def post(self, request, pk, format=None):
        # 질문 좋아요 추가/삭제

        user = get_object_or_404(User, pk=1) # JWT 배우기 전까지 임시로 1 할당
        question = get_object_or_404(Question, pk=pk)
        (obj, created) = LikeQuestion.objects.get_or_create(
            defaults={'created_at':timezone.now()},
            user=user,
            question=question,
        )
        if not created:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_201_CREATED)

class LikeAnswerRoot(views.APIView):
    def post(self, request, pk, format=None):
        # 답변 좋아요 추가/삭제

        user = get_object_or_404(User, pk=1) # JWT 배우기 전까지 임시로 1 할당
        answer = get_object_or_404(Answer, pk=pk)
        (obj, created) = LikeAnswer.objects.get_or_create(
            defaults={'created_at':timezone.now()},
            user=user,
            answer=answer,
        )
        if not created:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_201_CREATED)
