from django.db import models
from django.utils import timezone
from api.models import User



# Create your models here.
LANGUAGE_CHOICES=(
    (1, "KOR"),
    (2, "ENG"),
    (3, "JPN"),
    (4, "CHN"),
)

class Post(models.Model):
    #작성자 필드 추가 (User 외래키)
    user=models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=200)
    date=models.DateTimeField('date published')
    body=models.TextField()
    language=models.IntegerField(choices=LANGUAGE_CHOICES)
    likes=models.IntegerField()


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    comment_text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.comment_text
