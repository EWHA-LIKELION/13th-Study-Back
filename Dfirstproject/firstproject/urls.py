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
from community.views import List, detail, question_detail, new, create, delete, update_page, update, add_comment, like_question

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', List, name="main"),
    path('post/<int:pk>/', detail, name="detail"),
    path('question/<int:pk>', question_detail, name="question_detail"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('delete/<int:question_id>', delete, name="delete"),
    path('update_page/<int:question_id>', update_page, name='update_page'),
    path('update/<int:question_id>', update, name='update2'),
    path('<int:question_id>/comment', add_comment, name='add_comment'),
    path('question/<int:question_id>/like/', like_question, name='like_question'),
]
