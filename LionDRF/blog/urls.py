from django.urls import path
from .views import *

app_name='blog'

urlpatterns = [
    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/create/', PostList.as_view()),
    path('answer/create/', AnswerList.as_view()),
    path('answer/', AnswerList.as_view()),
    path('answer/<int:pk>/', AnswerDetail.as_view()),
    path('all/', AllList.as_view()), 
    path('comments/', Comment.as_view()),
]