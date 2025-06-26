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
    body = models.TextField()
    language = models.IntegerField(choices=LANGUAGE_CHOICES)

    def __str__ (self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username=models.CharField(max_length=20) #작성자 이름
    comment_text=models.TextField() #내용
    created_at=models.DateTimeField(default=timezone.now) #작성날짜


    def __str__(self):
        return self.comment_text
    

class Question(models.Model):
    #Question에 “작성자” 필드 추가 (User 외래키). settings의 AUTH_USER_MODEL에서 api.User를 참고하여 api의 models.py의 user를 가져온다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=1 )
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    body = models.TextField()
    language = models.IntegerField(choices=LANGUAGE_CHOICES)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_questions', blank=True)

    def __str__ (self):
        return self.title
    
class Answer(models.Model):
    #Answer에 “작성자” 필드 추가 (User 외래키). settings의 AUTH_USER_MODEL에서 api.User를 참고하여 api의 models.py의 user를 가져온다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=1 ) 
    question=models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    username=models.CharField(max_length=20) #작성자 이름
    answer_text=models.TextField() #내용
    created_at=models.DateTimeField(default=timezone.now) #작성날짜
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_answers', blank=True)


    def __str__(self):
        return self.answer_text
    



