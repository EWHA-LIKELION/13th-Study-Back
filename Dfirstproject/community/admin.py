from django.contrib import admin
from .models import Post, Comment, Hashtag
from .models import Question

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(Question)

#admin.site.register(Comment_Q)