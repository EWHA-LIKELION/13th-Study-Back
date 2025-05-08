"""
URL configuration for firstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from community.views import *
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('community', list, name='list'),
    path('community/<int:community_id>', detail, name='detail'),

    path('qna', get_question_list, name='get_question_list'),
    path('qna/<int:question_id>', get_question_detail, name='get_question_detail'),
    path('qna/create', get_question_create, name='get_question_create'),
    path('qna/<int:question_id>/update', get_question_update, name='get_question_update'),

    path('question/create', post_question_create, name='post_question_create'),
    path('question/<int:question_id>/update', post_question_update, name='post_question_update'),
    path('question/<int:question_id>/delete', delete_question, name='delete_question'),
 
    path('answer/create', post_answer_create, name='post_answer_create'),
    path('answer/<int:answer_id>/update', post_answer_update, name='post_answer_update'),
    path('answer/<int:answer_id>/delete', delete_answer, name='delete_answer'),

    path('question/<int:question_id>/like', post_likequestion_createdelete, name='post_likequestion_createdelete'),

    path('answer/<int:answer_id>/like', post_likeanswer_createdelete, name='post_likeanswer_createdelete'),

    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]
