from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True

class Community(Post):
    pass

class Question(Post):
    username = models.CharField(max_length=10, blank=True)
    status = models.BooleanField()

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = models.TextField()
    username = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content