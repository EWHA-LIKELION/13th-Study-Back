from django import forms
from .models import Question, Comment

class Questionform(forms.ModelForm):
  class Meta:
    model=Question
    fields=['title', 'content', 'photo']

class Commentform(forms.ModelForm):
  class Meta:
    model=Comment
    fields=['comment_text'] 