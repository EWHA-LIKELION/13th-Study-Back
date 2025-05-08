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
import community.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', community.views.List, name="main"),
    path('<int:pk>', community.views.detail, name="detail"),
    path('question_list/', community.views.question_list, name='question_list'),
    path('question/<int:pk>/', community.views.question_detail, name='question_detail'),
    path('new/', community.views.new, name="new"),
    path('create/', community.views.create, name="create"),
    path('delete/<int:question_id>/', community.views.delete, name="delete"),
    path('update_page/<int:question_id>', community.views.update_page, name='update_page'),
    path('update/<int:question_id>', community.views.update, name='update2'),
    path('question/<int:question_id>/add_comment/', community.views.add_comment, name='add_comment'),
    path('accounts/login', accounts.views.login_view, name='login'),
    path('accounts/logout', accounts.views.logout_view, name='logout'),
    path('accounts/signup', accounts.views.signup_view, name="signup"),
     path('<int:question_id>/likes/', community.views.likes, name='likes'),
]


