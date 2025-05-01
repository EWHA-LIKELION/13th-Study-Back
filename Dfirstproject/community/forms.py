from django import forms
from community.models import Post
from community.models import Question
from community.models import CommentForPost, CommentForQuestion

class Postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title', 'content']

class Questionform(forms.ModelForm):
    class Meta:
        model=Question
        fields=['title','content']

class CommentForPostform(forms.ModelForm):
    class Meta:
        model=CommentForPost
        fields=['username', 'comment_text']

class CommentForQuestionform(forms.ModelForm):
    class Meta:
        model=CommentForQuestion
        fields=['username', 'comment_text']
