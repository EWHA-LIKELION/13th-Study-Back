from django.db import models

# Create your models here.

class Post(models.Model):
    title=models.CharField('Title', max_length=50, blank=True)
    upload_time=models.DateTimeField(unique=True)
    content=models.TextField()

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]
    

class Question(models.Model):
    title=models.CharField('Title', max_length=50, blank=True)
    upload_time=models.DateTimeField(unique=True)
    content=models.TextField()

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]

