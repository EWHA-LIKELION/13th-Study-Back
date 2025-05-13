from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=20)

    def __str__(self):
        return self.hashtag

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    hashtag = models.ManyToManyField(Hashtag)

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
    
class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='like_question', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name+" 님이 "+self.question.title+" 질문을 좋아합니다."
    
class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='like_answer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name+" 님이 "+self.answer.pk+" 답변을 좋아합니다."