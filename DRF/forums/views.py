from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Prefetch
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer
from .serializers import CommunitySerializer, QuestionSerializer, AnswerSerializer

def add_hashtag(instance):
    hashtags = [word for word in instance.content.split() if word.startswith('#')]
    for hashtag in hashtags:
        (obj, created) = Hashtag.objects.get_or_create(hashtag=hashtag)
        instance.hashtag.add(obj)

class CommunityRoot(APIView):
    def get(self, request, format=None):
        # 커뮤니티 게시물 목록 조회

        query_string_search = request.query_params.get('search')

        condition = Q()
        if query_string_search:
            condition &= (Q(title__contains=query_string_search) | Q(content__contains=query_string_search))
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
    
class CommunityPk(APIView):
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
        
class QuestionRoot(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

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
            condition &= (Q(title__contains=query_string_search) | Q(content__contains=query_string_search))
        if question_status != None:
            condition &= Q(status=question_status)
        questions = Question.objects.filter(condition).order_by('-created_at')

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # 질문 게시물 추가

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                created_at=timezone.now(),
                writer=request.user,
            )
            add_hashtag(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionMy(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # 내가 작성한 질문 게시물 목록 조회

        questions = Question.objects.filter(writer=request.user).order_by('-created_at')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionPk(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        # 질문 게시글 상세 조회

        question = get_object_or_404(
            Question.objects.annotate(
                likes_count=Count('likes', distinct=True)
            ).prefetch_related(
                Prefetch(
                    'answers',
                    queryset=Answer.objects.annotate(likes_count=Count('likes'))
                )
            ),
            pk=pk
        )
        serializer = QuestionSerializer(question)

        is_liked = LikeQuestion.objects.filter(
            user=request.user,
            question=question,
        ).exists()

        return Response(serializer.data|{"is_liked":is_liked}, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        # 질문 게시글 수정

        question = get_object_or_404(Question, pk=pk)
        if question.writer == request.user:
            serializer = QuestionSerializer(question, data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                instance.hashtag.clear()
                add_hashtag(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        # 질문 게시글 삭제

        question = get_object_or_404(Question, pk=pk)
        if question.writer == request.user:
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

class AnswerRoot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # 답변 게시글 추가

        query_string_question_id = request.query_params.get('question_id')
        question = get_object_or_404(Question, pk=query_string_question_id)
        
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_at=timezone.now(),
                writer=request.user,
                question=question,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerMy(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # 내가 작성한 답변 게시물 목록 조회

        answers = Answer.objects.filter(writer=request.user).order_by('-created_at')
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AnswerPk(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        # 답변 게시글 수정

        answer = get_object_or_404(Answer, pk=pk)
        if answer.writer == request.user:
            serializer = AnswerSerializer(answer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        # 답변 게시글 삭제

        answer = get_object_or_404(Answer, pk=pk)
        if answer.writer == request.user:
            answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

class LikeQuestionRoot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        # 질문 좋아요 추가/삭제

        question = get_object_or_404(Question, pk=pk)
        (obj, created) = LikeQuestion.objects.get_or_create(
            defaults={'created_at':timezone.now()},
            user=request.user,
            question=question,
        )
        if not created:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_201_CREATED)

class LikeAnswerRoot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        # 답변 좋아요 추가/삭제

        answer = get_object_or_404(Answer, pk=pk)
        (obj, created) = LikeAnswer.objects.get_or_create(
            defaults={'created_at':timezone.now()},
            user=request.user,
            answer=answer,
        )
        if not created:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_201_CREATED)
