from django.urls import path
from .views import *

app_name = 'forums'

urlpatterns = [
    path('community', CommunityList.as_view()),
    path('community/<int:pk>', CommunityDetail.as_view()),

    path('question', QuestionList.as_view()),
    path('question/<int:pk>', QuestionDetail.as_view()),
    path('question/<int:pk>/like', LikeQuestionView.as_view()),

    path('answer', AnswerView.as_view()),
    path('answer/<int:pk>', AnswerDetail.as_view()),
    path('answer/<int:pk>/like', LikeAnswerView.as_view()),
]