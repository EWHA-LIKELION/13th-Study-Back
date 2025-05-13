from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, blank=True)
    upload_time = models.DateTimeField(unique = True) # upload_time은 중복되면 안되므로 unique = True
    content = models.TextField()
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    title = models.CharField(max_length=50, blank=True)
    upload_time = models.DateTimeField(unique = True) # 작성 날짜시간
    content = models.TextField() # 내용
    hashtag = models.ManyToManyField('Hashtag', blank=True) # 해시태그
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    photo = models.ImageField(blank=True, null=True, upload_to = "post_photo")
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    comment_text=models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def approve(self):
        self.save()
        
    def __str__ (self) :
        return self.comment_text
    
class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100)
    
    def __str__(self):
        return self.hashtag
    

    
