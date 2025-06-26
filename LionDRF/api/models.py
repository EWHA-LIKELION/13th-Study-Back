from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique = True)
    phonenumber = PhoneNumberField(verbose_name="휴대폰 번호", unique=True, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)