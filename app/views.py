from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from math import floor

from .forms import SetPassForm, UserRegistrationForm
from .models import *


def main(request):
    tests = Test.objects.all()
    return render(request, 'app/main.html', {'tests': tests})


@login_required(login_url='app:login')
def test_view(request, id):
    test = get_object_or_404(Test, id=id)
    username = request.user.username
    user = get_user_model().objects.filter(username=username).first()
    prof = get_prof(user)
    que_id = prof.que_id
    questions = QuestionList.objects.filter(test=test)
    end = len(questions)

    if request.method == 'POST':
        r = updtae_result(request, que_id[id], questions, prof, id)
        if r != -1:
            que_id[id] += 1
            prof.que_id = que_id
            prof.save()
            if que_id[id] >= end:
                return redirect(str(id) + '/result')
            return redirect('/test/' + str(id))

    now = que_id[id]
    question = questions[now].question
    answers = Answer.objects.filter(question=question)

    return render(request, 'app/question.html', {"question": question, "test": test, "que_id":que_id,
                                                 "answers": answers, "now": now+1, "end": end})


def updtae_result(request, id, questions, prof, test_id):
    answers = Answer.objects.filter(question=questions[id].question)
    res, null = True, True
    for answer in answers:
        if request.POST.get(str(answer.id)):
            null = False
            if not answer.is_right:
                res = False
    if null:
        return -1
    if res:
        corr = prof.count_corr
        corr[test_id] += 1
        prof.count_corr = corr
        prof.save()
    return 0


@login_required(login_url='app:login')
def result_view(request, id):
    test = get_object_or_404(Test, id=id)
    username = request.user.username
    user = get_user_model().objects.filter(username=username).first()
    prof = get_prof(user)
    questions = QuestionList.objects.filter(test=test)
    end = len(questions)
    que_id = prof.que_id

    if que_id[id] < end:
        return redirect('/')

    corr = prof.count_corr[id]
    prof.count_corr[id] = 0
    prof.que_id[id] = 0
    prof.count_test += 1
    prof.count_ok += corr
    prof.count_total += end
    prof.save()

    return render(request, 'app/result.html', {"test": test, "corr": corr, "total": end, "prec": get_prec(corr, end)})


@login_required(login_url='app:login')
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPassForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:login')

    form = SetPassForm(user)
    return render(request, 'registration/password_change.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/reg.html', {"form": form})


@login_required(login_url='app:login')
def profile(request):
    username = request.user.username
    user = get_user_model().objects.filter(username=username).first()
    prof = get_prof(user)
    return render(request, 'registration/profile.html', {"prof": prof, "user": user, "prec": get_prec(prof.count_ok, prof.count_total)})


def get_prec(a, b):
    if b == 0:
        return "-"
    return floor((a / b) * 100)


def get_prof(user):
    try:
    	prof = get_object_or_404(Profile, user=user)
    except:
    	Profile.objects.create(user=user)
    	prof = get_object_or_404(Profile, user=user)
    return prof
