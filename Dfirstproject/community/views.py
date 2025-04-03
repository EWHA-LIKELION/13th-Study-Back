from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from community.models import Post
from community.models import Question

# Create your views here.

def List(request):
    posts = Post.objects #posts는 변수
    questions = Question.objects
    return render(request, 'list.html', {'posts':posts, 'questions':questions})

def delete(request, post_id):
    post_delete=get_object_or_404(Post, pk=post_id)
    post_delete.delete()
    return redirect('list')

def delete_question(request, question_id):
    question_delete=get_object_or_404(Question, pk=question_id)
    question_delete.delete()
    return redirect('list')

def detail_post(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'detail.html', {'post':post})

def detail_question(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'detail.html', {'question':question})

def new(request):
    return render(request, 'new.html')

def create(request):
    new_post=Post()
    new_post.title=request.POST['title']
    new_post.content=request.POST['body']
    new_post.upload_time=timezone.now()
    new_post.save()
    return redirect('list')

def new_question(request):
    return render(request, 'new_question.html')

def create_question(request):
    new_question=Question()
    new_question.title=request.POST['title']
    new_question.content=request.POST['body']
    new_question.upload_time=timezone.now()
    new_question.save()
    return redirect('list')

def update_page(request, post_id):
    post_update=get_object_or_404(Post, pk=post_id)
    return render(request, 'update.html', {'post_update':post_update})

def update(request, post_id):
    post_update=get_object_or_404(Post, pk=post_id)
    post_update.title=request.POST['title']
    post_update.content=request.POST['body']
    post_update.save()
    return redirect('list')

def update_q_page(request, question_id):
    question_update=get_object_or_404(Question, pk=question_id)
    return render(request, 'update_q.html', {'question_update':question_update})

def update_q(request, question_id):
    question_update=get_object_or_404(Question, pk=question_id)
    question_update.title=request.POST['title']
    question_update.content=request.POST['body']
    question_update.save()
    return redirect('list')