from django.contrib import admin
from community.models import User, Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer

# Register your models here.

admin.site.register(User)
admin.site.register(Hashtag)
admin.site.register(Community)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)