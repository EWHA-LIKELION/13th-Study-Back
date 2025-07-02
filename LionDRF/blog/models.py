from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
LANGUAGE_CHOICES = (
    (1, "KOR"),
    (2, "ENG"),
    (3, "JPN"),
    (4, "CHN"),
)



class Post(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE) #작성자 필드 추가
    body = models.TextField()
    language = models.IntegerField(choices=LANGUAGE_CHOICES)
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True) #좋아요 필드 추가

    def __str__ (self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE) #작성자 필드 추가
    # username=models.CharField(max_length=20)
    comment_text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True) #좋아요 필드 추가

    def __str__(self):
        return self.comment_text

