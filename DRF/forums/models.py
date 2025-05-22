from django.db import models
from django.utils import timezone
from accounts.models import User

class Hashtag(models.Model):
    hashtag = models.CharField()

    def __str__(self):
        return self.hashtag

class Post(models.Model):
    writer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField()
    hashtag = models.ManyToManyField(
        Hashtag,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='post/image',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True

class Community(Post):
    pass

class Question(Post):
    status = models.BooleanField()

class Answer(models.Model):
    writer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    def __str__(self):
        return self.content
    
class LikeQuestion(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    question = models.ForeignKey(
        Question,
        related_name='likes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='like_question',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.first_name} 님이 "{self.question.title}" 질문을 좋아합니다.'
    
class LikeAnswer(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    answer = models.ForeignKey(
        Answer,
        related_name='likes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='like_answer',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.first_name} 님이 "{self.answer.content}" 답변을 좋아합니다.'