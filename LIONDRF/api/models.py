from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  email = models.EmailField(max_length = 100, unique = True)
  birth_date = models.DateField(null=True, blank=True) 
  phone_number = models.CharField(max_length=20, null=True, blank=True)  

