from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('create/', PostList.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('posts/<int:post_id>/like/', LikePostView.as_view()),
    path('comments/<int:comment_id>/like/', LikeCommentView.as_view()),
]