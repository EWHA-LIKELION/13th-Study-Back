from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
<<<<<<< main
    path('create/', PostList.as_view()),

    path('comments/', CommentList.as_view()),             # POST (댓글 생성)
    path('comments/<int:pk>/', CommentDetail.as_view()),

    path('questions/', QuestionList.as_view()),
    path('questions/<int:pk>/', QuestionDetail.as_view()),

    path('answers/', AnswerList.as_view()),             # POST (답글 생성)
    path('answers/<int:pk>/', AnswerDetail.as_view()),

    path('myquestions/', MyQuestionList.as_view()),
    path('myanswers/', MyAnswerList.as_view()),

    path('questions/create/', QuestionCreateAPIView.as_view()),
    path('answers/create/', AnswerCreateAPIView.as_view()),

    path('questions/<int:pk>/like/', QuestionLikeView.as_view()),
    path('answers/<int:pk>/like/', AnswerLikeView.as_view()),

=======
    path('create/', PostList.as_view())
>>>>>>> 2ewyeonwoo3
]