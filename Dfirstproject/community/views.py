from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Community, Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.

def list(request):
    posts = Community.objects.filter(created_at__lte = timezone.now()).order_by('created_at')
    return render(request, 'list.html', {'posts':posts})

def detail(request, community_id):
    post = get_object_or_404(Community, pk=community_id)
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
        questions = Question.objects.filter(status = 상태).only('title', 'created_at', 'username', 'status').order_by('-created_at')
    else:
        questions = Question.objects.only('title', 'created_at', 'username', 'status').order_by('-created_at')
    return render(request, 'question_list.html', {'questions':questions})

def get_question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    help_questions = Question.objects.filter(status = False).only('status').order_by('-created_at')
    return render(request, 'question_detail.html', {'question':question, 'help_questions':help_questions})

def get_question_create(request):
    form = QuestionForm()
    return render(request, 'question_create.html', {'form':form})
    
def post_question_create(request):
    form = QuestionForm(request.POST, request.FILES)
    if form.is_valid():
        created_question = form.save(commit=False)
        created_question.created_at = timezone.now()
        created_question.save()
        return redirect('get_question_detail', created_question.id)
    return redirect('get_question_list')

def get_question_update(request, question_id):
    form = QuestionForm()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question_update.html', {'form':form, 'question':question})

def post_question_update(request, question_id):
    prev_question = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(request.POST, request.FILES, instance=prev_question)
    if form.is_valid():
        updated_question = form.save(commit=False)
        updated_question.save()
        return redirect('get_question_detail', updated_question.id)
    return redirect('get_question_list')

def delete_question(requset, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('get_question_list')

def post_answer_create(request):
    question_id = request.GET.get('question_id')
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(request.POST)
    if form.is_valid():
        created_answer = form.save(commit=False)
        created_answer.question = question
        created_answer.created_at = timezone.now()
        created_answer.save()
        return redirect('get_question_detail', created_answer.question.id)
    return redirect('get_question_detail', question.id)

def post_answer_update(request, answer_id):
    prev_answer = get_object_or_404(Answer, pk=answer_id)
    form = AnswerForm(request.POST, instance=prev_answer)
    if form.is_valid():
        updated_answer = form.save(commit=False)
        updated_answer.save()
        return redirect('get_question_detail', updated_answer.question.id)
    return redirect('get_question_detail', prev_answer.question.id)

def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('get_question_detail', answer.question.id) # answer.question.id는 최종 응답 전까지 메모리에 캐시되어 있음.