from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    nickname=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    gender=models.CharField(max_length=50)