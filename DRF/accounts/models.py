from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Part(models.IntegerChoices):
        PLAN = 1, '기획'
        DESIGN = 2, '디자인'
        FRONTEND = 3, '프론트엔드'
        BACKEND = 4, '백엔드'
        AI = 5, 'AI'

    class Level(models.IntegerChoices):
        BABYLION = 1, '아기사자'
        MANAGER = 2, '운영진'
    
    image = models.ImageField(
        upload_to='user',
        null=True,
        blank=True,
    )
    part = models.PositiveSmallIntegerField(
        choices=Part.choices,
    )
    generation = models.PositiveSmallIntegerField()
    level = models.PositiveSmallIntegerField(
        choices=Level.choices,
    )

    REQUIRED_FIELDS = ['part','generation','level']