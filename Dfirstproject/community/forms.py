from django import forms
from community.models import Post
from community.models import Question

class Postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title', 'content']

class Questionform(forms.ModelForm):
    class Meta:
        model=Question
        fields=['title','content']