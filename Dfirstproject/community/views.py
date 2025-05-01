from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from community.models import Post, Hashtag
from community.models import Question
from community.forms import Postform, Questionform, Commentform

# Create your views here.

def List(request):
    posts = Post.objects #posts는 변수
    questions = Question.objects.all()
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
    post_hashtag = post.hashtag.all()
    return render(request, 'detail.html', {'post':post, 'hashtag': post_hashtag})

def detail_question(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'detail.html', {'question':question})

def new(request):
    form=Postform() #추가코드
    return render(request, 'new.html', {'form':form})
    #return render(request, 'new.html')

def create(request):
    form = Postform(request.POST, request.FILES)
    if form.is_valid():
        new_post=form.save(commit=False)
        new_post.upload_time=timezone.now()
        new_post.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(', ')

        for tag in hashtag:
            new_hashtag = Hashtag.objects.get_or_create(hashtag = tag)
            new_post.hashtag.add(new_hashtag[0])
        return redirect('detail_post', new_post.id)
    return redirect('list')

def new_question(request):
    form=Questionform() #추가코드
    return render(request, 'new_question.html', {'form':form})
    #return render(request, 'new_question.html')

def create_question(request):
    form = Questionform(request.POST, request.FILES)
    if form.is_valid():
        new_question=form.save(commit=False)
        new_question.upload_time=timezone.now()
        new_question.save()
        return redirect('detail_question', new_question.id)
    return redirect('list')

def update_page(request, post_id):
    post_update=get_object_or_404(Post, pk=post_id)
    return render(request, 'update.html', {'post_update':post_update})

def update(request, post_id):
    post_update=get_object_or_404(Post, pk=post_id)
    post_update.title=request.POST['title']
    post_update.content=request.POST['content']
    post_update.save()
    return redirect('list')

def update_q_page(request, question_id):
    question_update=get_object_or_404(Question, pk=question_id)
    return render(request, 'update_q.html', {'question_update':question_update})

def update_q(request, question_id):
    question_update=get_object_or_404(Question, pk=question_id)
    question_update.title=request.POST['title']
    question_update.content=request.POST['content']
    question_update.save()
    return redirect('list')

def add_comment(request, post_id):
    post = get_object_or_404(Post, pk = post_id)

    if request.method == 'POST':
        form = Commentform(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail_post', post_id)
    
    else:
        form = Commentform()

    return render(request, 'add_comment.html', {'form':form})