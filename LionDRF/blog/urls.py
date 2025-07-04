from django.urls import path
from .views import *

app_name='blog'

urlpatterns=[
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('create/', PostList.as_view()),
    path('lang/', PostListLang.as_view()),  
    path('comments/', Comment.as_view()),
    path('comments/<int:pk>', CommentView.as_view()),
    path('post/<int:pk>/like/', LikePostView.as_view()),
    path('comment/<int:pk>/like/', LikeCommentView.as_view()),
]