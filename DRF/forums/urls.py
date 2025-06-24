from django.urls import path
from .views import *

app_name = 'forums'

urlpatterns = [
    path('community', CommunityRoot.as_view()),
    path('community/<int:pk>', CommunityPk.as_view()),

    path('question', QuestionRoot.as_view()),
    path('question/my', QuestionMy.as_view()),
    path('question/<int:pk>', QuestionPk.as_view()),
    path('question/<int:pk>/like', LikeQuestionRoot.as_view()),

    path('answer', AnswerRoot.as_view()),
    path('answer/my', AnswerMy.as_view()),
    path('answer/<int:pk>', AnswerPk.as_view()),
    path('answer/<int:pk>/like', LikeAnswerRoot.as_view()),
]