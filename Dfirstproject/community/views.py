from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Community, Question
from .forms import QuestionForm

# Create your views here.

def list(request):
    posts = Community.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time')
    return render(request, 'list.html', {'posts':posts})

def detail(request, id):
    post = get_object_or_404(Community, pk=id)
    return render(request, 'detail.html', {'post':post})

def get_question_list(request):
    query_string_상태 = request.GET.get('상태')
    if query_string_상태 == '도와주세요':
        상태 = False
    elif query_string_상태 == '해결됐어요':
        상태 = True
    else:
        상태 = None
    if 상태 != None:
        questions = Question.objects.filter(status = 상태).only('title', 'upload_time', 'name', 'status').order_by('-upload_time')
    else:
        questions = Question.objects.only('title', 'upload_time', 'name', 'status').order_by('-upload_time')
    return render(request, 'question_list.html', {'questions':questions})

def get_question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    help_questions = Question.objects.filter(status = False).only('status').order_by('-upload_time')
    return render(request, 'question_detail.html', {'question':question, 'help_questions':help_questions})

def get_question_create(request):
    form = QuestionForm()
    return render(request, 'question_create.html', {'form':form})
    
def post_question_create(request):
    form = QuestionForm(request.POST, request.FILES)
    if form.is_valid():
        created_question = form.save(commit=False)
        created_question.upload_time = timezone.now()
        created_question.save()
        return redirect('get_question_detail', created_question.id)
    return redirect('get_question_list')

def get_question_update(request, id):
    form = QuestionForm()
    question = get_object_or_404(Question, pk=id)
    return render(request, 'question_update.html', {'form':form, 'question':question})

def post_question_update(request, id):
    prev_question = get_object_or_404(Question, pk=id)
    form = QuestionForm(request.POST, request.FILES, instance=prev_question)
    if form.is_valid():
        updated_question = form.save(commit=False)
        updated_question.save()
        return redirect('get_question_detail', updated_question.id)
    return redirect('get_question_list')

def delete_question(requset, id):
    question = get_object_or_404(Question, pk=id)
    question.delete()
    return redirect('get_question_list')