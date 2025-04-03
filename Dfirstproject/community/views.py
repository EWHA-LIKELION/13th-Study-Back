from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from community.models import Post
from community.models import Question
from community.forms import Questionform
# Create your views here.

def List(request):
  posts = Post.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time')
  questions = Question.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time')
  return render(request, 'list.html', {'posts':posts, 'questions': questions,})

def detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'detail.html', {'post':post})

def question_detail(request, pk):
  question = get_object_or_404(Question, pk=pk)
  return render(request, 'question_detail.html', {'question': question})

def new(request):
  form=Questionform()
  return render(request, 'new.html', {'form':form})

def create(request):
  form = Questionform(request.POST, request.FILES)
  if form.is_valid():
    new_community=form.save(commit=False)
    new_community.upload_time=timezone.now()
    new_community.save()
    return redirect('question_detail', new_community.id)
  return redirect('main')

def delete(request, question_id):
  community_delete=get_object_or_404(Question, pk=question_id)
  community_delete.delete()
  return redirect('main')

def update_page(request, question_id):
  community_update=get_object_or_404(Question, pk=question_id)
  return render(request, 'update.html', {'community_update': community_update})

def update(request, question_id):
  community_update=get_object_or_404(Question, pk=question_id)
  community_update.title=request.POST['title']
  community_update.content=request.POST['content']
  community_update.save()
  return redirect('main')