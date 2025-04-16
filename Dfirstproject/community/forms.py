from django import forms
from .models import Question, Comment

class Questionform(forms.ModelForm):
  class Meta:
    model=Question
    fields=['title', 'content']

class Commentform(forms.ModelForm):
  class Meta:
    model=Comment
    fields=['username', 'comment_text']