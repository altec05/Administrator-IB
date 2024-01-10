from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import date
from certs.models import Cerificate
from changes.models import Version
from licenses.models import License, Installation, InstallSoft
from workers.models import Worker
from applications.models import Application
from .forms import *


def index(request):
    return render(request, 'index.html')


# def admin_index(request):
#     return redirect('/admin/')


def red_to_admin(request):
    return redirect('admin')


def red_admin(request):
    return redirect('admin')


def red_certs(request):
    return redirect('/admin/certs/cerificate/')


def password_reset(request):
    return HttpResponse(f"<h2>Смена пароля производится только администратором!</h2><br><a href='/login' class='text-primary fw-bold'>Назад</a>")


def pick_worker(request):
    if request.method == "POST":
        choice = request.POST.get('worker_choice')
        print("choice=", request.POST)
        if choice:
            # main = Worker.objects.get(id=choice)
            #
            # certs = Cerificate.objects.filter(subject=main.pk)
            # applications = Application.objects.filter(subject=main.pk)
            # licenses = License.objects.filter(installation__subject=main.pk)
            # workers = Worker.objects.filter(id=main.pk)
            #
            # data = {"certs": certs, "applications": applications, "licenses": licenses, "workers": workers, 'main': main}
            #
            # # return HttpResponse(f"<h2>Записи по сотруднику {main}</h2>")
            # return render(request, "lists_by_worker/pick_worker.html", context=data)
            return redirect('by_worker', choice)
        else:
            return HttpResponse(f"<h2>Вы не выбрали сотрудника!</h2>")
    else:
        # all_workers = Worker.objects.filter(visibility=True).order_by('full_name')
        # workers = []
        # for worker in all_workers:
        #     workers.append((worker.id, worker.full_name))

        worker_pick_form = PickWorkerForm()
        return render(request, "lists_by_worker/pick_worker.html", {"form": worker_pick_form})
        # return render(request, "lists_by_worker/pick_worker.html", {'workers': workers})


def lists_by_worker(request, worker_id):
    # if request.user.is_authenticated:
    #     return redirect('profile')
    # main = Worker.objects.get(full_name='Пирогова Александра Валерьевна')
    main = Worker.objects.get(id=worker_id)
    # if request.method == 'GET':
    certs = Cerificate.objects.filter(subject=main.pk)
    applications = Application.objects.filter(subject=main.pk)
    licenses = License.objects.filter(installation__subject=main.pk)
    installations = Installation.objects.filter(subject=main.pk)
    workers = Worker.objects.filter(id=main.pk)

    data = {"certs": certs, "applications": applications, "licenses": licenses, 'installations': installations, "workers": workers, 'main': main, 'len_applications': len(applications), 'len_licenses': len(licenses), 'len_certs': len(certs)}
    return render(request, "lists_by_worker/lists_by_worker.html", context=data)
    # return render(request, 'lists_by_worker.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'profile.html')


# Страница авторизации
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользователь с таким логином не найден!')
            print('Пользователь с таким логином не найден!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')

    return render(request, 'registration/login.html')


