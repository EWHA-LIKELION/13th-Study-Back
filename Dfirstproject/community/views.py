from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from community.models import Post, Question
from .forms import Questionform


# Create your views here.

def List(request):
    posts = Post.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time') # posting 속 객체를 게시물 업로드 순서에 따라 배열
    questions = Question.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time') # posting 속 객체를 게시물 업로드 순서에 따라 배열
    return render(request, 'list.html', {'posts' : posts, 'questions' : questions}) # 화면에 보이게 렌더링

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # 게시글을 업로드 할 때마다 매기는 번호
    return render(request, 'detail.html', {'post':post})

def question_list(request):
    questions = Question.objects.filter(upload_time__lte=timezone.now()).order_by('upload_time')
    return render(request, 'question_list.html', {'questions': questions})

def question_detail(request, pk):
    questions = get_object_or_404(Question, pk=pk) # 게시글을 업로드 할 때마다 매기는 번호
    return render(request, 'question_detail.html', {'questions':questions}) # 화면에 보이게 렌더링

def new(request): # new.html 렌더링
    form=Questionform()
    return render(request, 'new.html', {'form':form}) 

def create(request):
    form = Questionform(request.POST, request.FILES)
    if form.is_valid():
        new_question=form.save(commit=False) # 폼 내용 일시 저장
        new_question.upload_time = timezone.now()
        new_question.save()
        return redirect('question_detail', new_question.id)

def delete(request, question_id):
    question_delete=get_object_or_404(Question, pk=question_id)
    question_delete.delete()
    return redirect('main')

def update_page(request, question_id):
    question_update=get_object_or_404(Question,pk=question_id)
    return render(request, 'update.html', {'question_update':question_update})

def update(request, question_id):
    if request.method == 'POST':
        question_update = get_object_or_404(Question, pk=question_id)
        question_update.title = request.POST['title']
        question_update.content = request.POST['content']
        question_update.save()
        return redirect('main')
    else:
        return redirect('update_page', question_id=question_id)


