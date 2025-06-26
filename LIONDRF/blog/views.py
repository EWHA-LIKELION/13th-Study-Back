from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PostList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        post = Post.objects.all()
        
        keyword = request.GET.get('keyword')
        sort = request.GET.get('sort')

        if keyword:
            post = Post.objects.filter(title__icontains=keyword)
        else:
            post = Post.objects.all()

        # ?sort=title : 오름차순, ?sort=-title : 내림차순
        if sort in ['title', '-title', 'created_at', '-created_at']:
            post = post.order_by(sort)

        serializer = PostSerializer(post, many=True)
        return Response({
            'count': post.count(),
            'results': serializer.data
        })
        

        #입력받은 게시글 데이터를 시리얼라이저에 넣어 변환
        #데이터가 유효하면 저장하고 데이터와 상태코드를 반환
    def post(self, request, format=None):     

        serializer = PostSerializer(data=request.data)
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
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
   
    def put(self, request, pk, format=None):
        post=get_object_or_404(Post, pk=pk)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        post=get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"message":"게시물 삭제 성공"})
    


class CommentList(views.APIView):      
    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetail(views.APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response({"message": "댓글 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
    


class QuestionList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True, context={'request': request})
        return Response(serializer.data)
        
        #입력받은 게시글 데이터를 시리얼라이저에 넣어 변환
        #데이터가 유효하면 저장하고 데이터와 상태코드를 반환
    def post(self, request, format=None):     
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 자신의 질문 전체 조회
class MyQuestionList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        questions = Question.objects.filter(user=user)
        serializer = QuestionSerializer(questions, many=True, context={'request': request}) 
        return Response(serializer.data)
    

class QuestionDetail(views.APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, context={'request': request}) 
        return Response(serializer.data)
   
    def put(self, request, pk, format=None):
        question=get_object_or_404(Question, pk=pk)
        if question.user != request.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer=QuestionSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        question=get_object_or_404(Question, pk=pk)
        if question.user != request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        question.delete()
        return Response({"message": "질문 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
    


class AnswerList(views.APIView):      
    def post(self, request, format=None):
        serializer=AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 자신의 전체 솔루션 조희
class MyAnswerList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        answers = Answer.objects.filter(user=user)
        serializer = AnswerSerializer(answers, many=True, context={'request': request})
        return Response(serializer.data)


class AnswerDetail(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        answer = self.get_object(pk)
        if answer.user != request.user:
            return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AnswerSerializer(answer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        answer = self.get_object(pk)
        if answer.user != request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        answer.delete()
        return Response({"message": "답변 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
    

class QuestionCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]  # 🔐 access token이 있어야 접근 가능

    def post(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class AnswerCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class QuestionLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        if request.user in question.likes.all():
            question.likes.remove(request.user)
            return Response({'message': '좋아요 취소'}, status=200)
        else:
            question.likes.add(request.user)
            return Response({'message': '좋아요 추가'}, status=200)


class AnswerLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            answer = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            return Response({"error": "답변이 존재하지 않습니다."}, status=404)

        user = request.user

        if user in answer.likes.all():
            answer.likes.remove(user)
            return Response({"message": "좋아요 취소됨", "likes_count": answer.likes.count()})
        else:
            answer.likes.add(user)
            return Response({"message": "좋아요 추가됨", "likes_count": answer.likes.count()})

    

    
