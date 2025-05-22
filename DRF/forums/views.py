from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from .models import Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer
from .serializers import CommunitySerializer, QuestionSerializer, AnswerSerializer

