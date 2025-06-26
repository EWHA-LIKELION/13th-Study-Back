from django.db import models
from django.utils import timezone

# Create your models here.
LANGUAGE_CHOICES = (
    (1, "KOR"),
    (2, "ENG"),
    (3, "JPN"),
    (4, "CHN"),
)

class Post(models.Model): # 질문
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    body = models.TextField()
    language = models.IntegerField(choices = LANGUAGE_CHOICES, default=1)
    user= models.ForeignKey('api.User', related_name='posts', on_delete=models.CASCADE)
    like_users = models.ManyToManyField('api.User', related_name='like_articles')
    def __str__(self):
        return self.title
    
class Answer(models.Model): # 답변
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='answers', on_delete=models.CASCADE)
    user= models.ForeignKey('api.User', related_name='answers', on_delete=models.CASCADE)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=1)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model): # post-댓글
    post=models.ForeignKey(Post, related_name = 'comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    comment_text = models.TextField()
    created_at=models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return self.comment_text
    


    
