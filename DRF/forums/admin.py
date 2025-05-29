from django.contrib import admin
from .models import Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer

admin.site.register(Hashtag)
admin.site.register(Community)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)