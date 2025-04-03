from django import forms
from .models import Question

class Questionform(forms.ModelForm):
  class Meta:
    model=Question
    fields=['title', 'content']