from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    nickname=models.CharField(max_length=100)
    university=models.CharField(max_length=50)
    major=models.CharField(max_length=50, default="null")
    semester=models.CharField(max_length=50, default="null")
    location=models.CharField(max_length=200)
