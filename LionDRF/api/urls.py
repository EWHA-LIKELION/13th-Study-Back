from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
]