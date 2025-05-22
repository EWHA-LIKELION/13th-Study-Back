from django.db import models

# Create your models here.
LANGUAGE_CHOICES=(
    (1, "KOR"),
    (2, "ENG"),
    (3, "JPN"),
    (4, "CHN"),
)

class Post(models.Model):
    title=models.CharField(max_length=200)
    date=models.DateTimeField('date published')
    body=models.TextField()
    language=models.IntegerField(choices=LANGUAGE_CHOICES)


    def __str__(self):
        return self.title
    