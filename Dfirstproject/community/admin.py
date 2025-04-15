from django.contrib import admin
from community.models import Community, Question, Answer

# Register your models here.

admin.site.register(Community)
admin.site.register(Question)
admin.site.register(Answer)