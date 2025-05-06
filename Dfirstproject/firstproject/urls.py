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
from community.views import List, Qdetail, detail, post_new, post_create, question_new, question_create, post_delete, question_delete, post_update, post_update_page, question_update, question_update_page, add_commentforpost, add_commentforquestion, post_like, question_like
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', List, name="main"),
    path('post/<int:pk>/', detail, name="detail"),
    path('question/<int:pk>/', Qdetail, name="Qdetail"),
    path('post_new/', post_new, name="post_new"),
    path('post_create/', post_create, name="post_create"),
    path('question_new/', question_new, name="question_new"),
    path('question_create/', question_create, name="question_create"),
    path('post_delete/<int:post_id>', post_delete, name='post_delete'),
    path('question_delete/<int:question_id>', question_delete, name='question_delete'),
    path('post_update/<int:post_id>', post_update, name='post_update'),
    path('post_update_page/<int:post_id>', post_update_page, name='post_update_page'),
    path('question_update/<int:question_id>', question_update, name='question_update'),
    path('question_update_page/<int:question_id>', question_update_page, name='question_update_page'),
    path('post/<int:post_id>/comment/', add_commentforpost, name='add_commentforpost'),
    path('question/<int:question_id>/comment/', add_commentforquestion, name='add_commentforquestion'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('question/<int:question_id>/like/', question_like, name='question_like'),
    path('accounts/login', accounts.views.login_view, name="login"),
    path('accounts/logout', accounts.views.logout_view, name="logout"),
    path('accounts/signup', accounts.views.singup_view, name="signup"),
]
