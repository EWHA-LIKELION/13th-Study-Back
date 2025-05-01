from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from community.models import Post
from community.models import Question
from community.models import Hashtag
from django.utils import timezone
from .forms import Postform, Questionform, CommentForPostform, CommentForQuestionform

# Create your views here.

def List(request):
    posts = Post.objects.filter(upload_time__lte=timezone.now()).order_by('upload_time')
    questions = Question.objects.filter(upload_time__lte=timezone.now()).order_by('upload_time')

    context = {
        'posts': posts,
        'questions': questions
    }
    return render(request, 'list.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_hashtag = post.hashtag.all()
    return render(request, 'post_detail.html', {'post':post, 'hashtag':post_hashtag})

def Qdetail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question_hashtag = question.hashtag.all()
    return render(request, 'question_detail.html', {'question':question, 'hashtag':question_hashtag})


#포스트 등록 함수 
def post_new(request):
    form=Postform()
    return render(request, 'post_new.html', {'Postform':form})

def post_create(request):
    form=Postform(request.POST, request.FILES)
    if form.is_valid():
        new_post=form.save(commit=False)
        new_post.upload_time=timezone.now()
        new_post.save()
        hashtags=request.POST['hashtags']
        hashtag = hashtags.split(', ')

        for tag in hashtag:
            new_hashtag=Hashtag.objects.get_or_create(hashtag=tag)
            new_post.hashtag.add(new_hashtag[0])
        return redirect('detail', new_post.id)
    return redirect('main')

#질문 등록 함수 
def question_new(request):
    form=Questionform()
    return render(request, 'question_new.html', {'Questionform':form})

def question_create(request):
    form=Questionform(request.POST, request.FILES)
    if form.is_valid():
        new_question=form.save(commit=False)
        new_question.upload_time=timezone.now()
        new_question.save()
        hashtags=request.POST['hashtags']
        hashtag = hashtags.split(', ')

        for tag in hashtag:
            new_hashtag=Hashtag.objects.get_or_create(hashtag=tag)
            new_question.hashtag.add(new_hashtag[0])
        return redirect('Qdetail', new_question.id)
    return redirect('main')

#포스트 삭제 함수
def post_delete(request, post_id):
    post_delete=get_object_or_404(Post,pk=post_id)
    post_delete.delete()
    return redirect('main')

#질문 삭제 함수
def question_delete(request, question_id):
    question_delete=get_object_or_404(Question,pk=question_id)
    question_delete.delete()
    return redirect('main')

#포스트 수정 함수
def post_update_page(request, post_id):
    post_update=get_object_or_404(Post,pk=post_id)
    return render(request, 'post_update.html', {'post_update':post_update})

def post_update(request, post_id):
    post_update=get_object_or_404(Post,pk=post_id)
    post_update.title=request.POST['title']
    post_update.content=request.POST['content']
    post_update.save()
    return redirect('main')

#질문 수정 함수
def question_update_page(request, question_id):
    question_update=get_object_or_404(Question,pk=question_id)
    return render(request, 'question_update.html', {'question_update':question_update})

def question_update(request, question_id):
    question_update=get_object_or_404(Question,pk=question_id)
    question_update.title=request.POST['title']
    question_update.content=request.POST['content']
    question_update.save()
    return redirect('main')
    
#포스트 댓글 함수
def add_commentforpost(request, post_id):
    post=get_object_or_404(Post, pk=post_id)

    if request.method=='POST':
        form=CommentForPostform(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('detail', pk=post.pk)
        
    else:
        form=CommentForPostform()
    return render(request, 'add_commentforpost.html',{'form':form, 'post':post,})

#질문 댓글 함수
def add_commentforquestion(request, question_id):
    question=get_object_or_404(Question, pk=question_id)

    if request.method=='POST':
        form=CommentForQuestionform(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.quesiton=question
            comment.save()
            return redirect('Qdetail', pk=question.pk)
        
    else:
        form=CommentForQuestionform()
    return render(request, 'add_commentforquestion.html',{'form':form, 'question':question,})

#포스트 좋아요 함수
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.likes_count += 1
        post.save()
    return redirect('detail', pk=post.pk)

#질문 좋아요 함수 
def question_like(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.likes_count += 1
        question.save()
    return redirect('Qdetail', pk=question.pk)