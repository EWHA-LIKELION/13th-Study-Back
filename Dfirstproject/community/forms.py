from django import forms
from .models import Question, Comment

class Questionform(forms.ModelForm):
  class Meta:
    model=Question
    fields=['title', 'content']

class Commentform(forms.ModelForm):
  class Meta:
    model=Comment
    fields=['comment_text'] #username 필드 제거 후 로그인 정보 바로 입력되게 설정정