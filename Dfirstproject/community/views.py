from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from community.models import Community,Question

# Create your views here.

def list(request):
    posts = Community.objects.filter(upload_time__lte = timezone.now()).order_by('upload_time')
    return render(request, 'pages/list.html', {'posts':posts})

def detail(request, id):
    post = get_object_or_404(Community, pk=id)
    return render(request, 'pages/detail.html', {'post':post})

def question_list(request):
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
    return render(request, 'pages/question_list.html', {'questions':questions})

def question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    help_questions = Question.objects.filter(status = False).only('status').order_by('-upload_time')
    return render(request, 'pages/question_detail.html', {'question':question, 'help_questions':help_questions})