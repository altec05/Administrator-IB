from django.shortcuts import render
from .models import License, ActOfInstall, Address


def show_acts(request):
    # получаем все значения модели
    data = ActOfInstall.objects.all()
    return render(request, 'show_acts.html', {'data': data})