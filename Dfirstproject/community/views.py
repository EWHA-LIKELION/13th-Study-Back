from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import User, Hashtag, Community, Question, Answer, LikeQuestion, LikeAnswer
from .forms import QuestionForm, AnswerForm

def home(request):
    return render(request, 'home.html')

# Community

## Read

def list(request):
    posts = Community.objects.filter(created_at__lte = timezone.now()).order_by('created_at')
    return render(request, 'list.html', {'posts':posts})

def detail(request, community_id):
    post = get_object_or_404(Community, pk=community_id)
    return render(request, 'detail.html', {'post':post})

# Question

## Create

def post_question_create(request):
    form = QuestionForm(request.POST, request.FILES)
    if form.is_valid():
        created_question = form.save(commit=False)
        created_question.created_at = timezone.now()
        created_question.save()

        created_hashtags = [word for word in created_question.content.split() if word.startswith('#')]
        for created_hashtag in created_hashtags:
            hashtag = Hashtag.objects.get_or_create(hashtag = created_hashtag)
            created_question.hashtag.add(hashtag[0])

        return redirect('get_question_detail', created_question.id)
    return redirect('get_question_list')

## Read

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
    return render(request, 'question_create.html')

def get_question_update(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question_update.html', {'question':question})

## Update

def post_question_update(request, question_id):
    prev_question = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(request.POST, request.FILES, instance=prev_question)
    if form.is_valid():
        updated_question = form.save(commit=False)
        updated_question.hashtag.clear()
        updated_question.save()

        updated_hashtags = [word for word in updated_question.content.split() if word.startswith('#')]
        for updated_hashtag in updated_hashtags:
            hashtag = Hashtag.objects.get_or_create(hashtag = updated_hashtag)
            updated_question.hashtag.add(hashtag[0])

        return redirect('get_question_detail', updated_question.id)
    return redirect('get_question_list')

## Delete

def delete_question(requset, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('get_question_list')

# Answer

## Create

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
    return redirect('get_question_detail', question_id)

## Update

def post_answer_update(request, answer_id):
    prev_answer = get_object_or_404(Answer, pk=answer_id)
    form = AnswerForm(request.POST, instance=prev_answer)
    if form.is_valid():
        updated_answer = form.save(commit=False)
        updated_answer.save()
        return redirect('get_question_detail', updated_answer.question.id)
    return redirect('get_question_detail', prev_answer.question.id)

## Delete

def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('get_question_detail', answer.question.id) # answer.question.id는 최종 응답 전까지 메모리에 캐시되어 있음.

# LikeQuestion

## Create & Delete (Toggle)

def post_likequestion_createdelete(request, question_id):
    user_id = request.GET.get('user_id')
    question = get_object_or_404(Question, pk=question_id)
    user = get_object_or_404(User, pk=user_id)
    obj, created = LikeQuestion.objects.get_or_create(question = question, user = user, defaults={'created_at':timezone.now()})
    if not created:
        obj.delete()
    return redirect('get_question_detail', question_id)

# LikeAnswer

## Create & Delete (Toggle)

def post_likeanswer_createdelete(request, answer_id):
    user_id = request.GET.get('user_id')
    answer = get_object_or_404(Answer, pk=answer_id)
    user = get_object_or_404(User, pk=user_id)
    obj, created = LikeAnswer.objects.get_or_create(answer = answer, user = user, defaults={'created_at':timezone.now()})
    if not created:
        obj.delete()
    return redirect('get_question_detail', answer.question.id)