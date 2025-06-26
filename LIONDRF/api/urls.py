from .views import *
from django.urls import path, include

app_name = 'api'

urlpatterns = [
  path('signup/',SignupView.as_view()),
  path('login/', LoginView.as_view()),
  
] 