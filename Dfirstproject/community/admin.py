from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Post)

admin.site.register(Question)

admin.site.register(CommentForPost)
admin.site.register(CommentForQuestion)

admin.site.register(Hashtag)

