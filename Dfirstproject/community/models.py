from django.db import models
from django.utils import timezone

# Create your models here.
class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100)

    def __str__(self):
        return self.hashtag

class Post(models.Model):
    title=models.CharField('Title', max_length=50, blank=True)
    upload_time=models.DateTimeField(unique=True)
    content=models.TextField()
    hashtag=models.ManyToManyField(Hashtag)
    likes_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]
    

class Question(models.Model):
    title=models.CharField('Title', max_length=50, blank=True)
    upload_time=models.DateTimeField(unique=True)
    content=models.TextField()
    hashtag=models.ManyToManyField(Hashtag)
    likes_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]


class CommentForPost(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    comment_text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment_text


class CommentForQuestion(models.Model):
    question=models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    comment_text=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment_text
