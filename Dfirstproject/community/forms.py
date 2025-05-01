from django import forms
from .models import Question, Comment, Post # post 폼도 만들긴 해야되는데....

class Questionform(forms.ModelForm):
    class Meta:
        model=Question
        fields=['title', 'content']
        
class Commentform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['username', 'comment_text']
        
        