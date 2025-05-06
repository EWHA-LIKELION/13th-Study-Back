from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Part(models.IntegerChoices):
        PLAN = 1
        DESIGN = 2
        FRONTEND = 3
        BACKEND = 4
        AI = 5

    class Level(models.IntegerChoices):
        BABYLION = 1
        MANAGER = 2
    
    university = models.CharField(max_length=50)
    generation = models.PositiveSmallIntegerField()
    part = models.PositiveSmallIntegerField(choices=Part.choices)
    level = models.PositiveSmallIntegerField(choices=Level.choices)