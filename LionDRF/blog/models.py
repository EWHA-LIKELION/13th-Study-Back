from django.db import models
from django.utils import timezone
from django.conf import settings

LANGUAGE_CHOICES = (
  (1, "KOR"),
  (2, "ENG"),
  (3, "JPN"),
  (4, "CHN"),
)

class Post(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE, null=True)
  title=models.CharField(max_length=200)
  date=models.DateTimeField('date published')
  body=models.TextField()
  language=models.IntegerField(choices=LANGUAGE_CHOICES)

  def __str__ (self):
    return self.title
    

class LikePost(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='liked_posts', on_delete=models.CASCADE, null=True)
  post=models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE, null=True)
  created_at=models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ('user', 'post')

  def __str__(self):
    return f"{self.user.username} liked '{self.post.title}'"

    
class Comment(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comments', on_delete=models.CASCADE, null=True)
  post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
  comment_text=models.TextField()
  created_at=models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.comment_text


class LikeComment(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='liked_comments', on_delete=models.CASCADE, null=True)
  comment=models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE, null=True)
  created_at=models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ('user', 'comment')

  def __str__(self):
    return f"{self.user.username} liked comment: '{self.comment.comment_text[:15]}...'"
