from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(max_length=100, unique=True)
    birth_date=models.DateField(max_length=100, null=True, blank=True) #생일 필드 추가 


