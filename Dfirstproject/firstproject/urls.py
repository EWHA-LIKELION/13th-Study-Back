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
from community.views import List, detail_post, detail_question, new, create, delete, update_page, update, new_question, create_question, delete_question, update_q_page, update_q

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', List, name="list"),
    path('post/<int:post_id>/', detail_post, name="detail_post"),
    #path('', List_question, name="list_question"),
    path('question/<int:question_id>/', detail_question, name="detail_question"),
    
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('delete/<int:post_id>/', delete, name='delete'),
    path('update_page/<int:post_id>/', update_page, name='update_page'),
    path('update/<int:post_id>/', update, name='update2'),

    path('question/new/', new_question, name="new_question"),
    path('question/create/', create_question, name="create_question"),
    path('question/delete/<int:question_id>/', delete_question, name='delete_question'),
    path('question/update_page/<int:question_id>/', update_q_page, name='update_q_page'),
    path('question/update/<int:question_id>/', update_q, name='update_q'),
]
