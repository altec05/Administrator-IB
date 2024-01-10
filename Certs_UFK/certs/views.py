# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib import messages
# from django.http import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required
# from datetime import date
# from django.core.files.storage import FileSystemStorage
# from django.views.generic import CreateView
# from .forms import CertForm
# from .models import Cerificate
#
#
# class CertCreate(CreateView):
#     # Модель куда выполняется сохранение
#     model = Cerificate
#     # Класс на основе которого будет валидация полей
#     form_class = CertForm
#     # Выведем все существующие записи на странице
#     extra_context = {'certs': Cerificate.objects.all()}
#     # Шаблон с помощью которого
#     # будут выводиться данные
#     template_name = 'certs/get_new_certificate.html'
#     # На какую страницу будет перенаправление
#     # в случае успешного сохранения формы
#     success_url = '/done'
#
#
# def get_new_certificate(request):
#     if request.method == 'POST' and request.FILES:
#         # получаем загруженный файл
#         file = request.FILES
#         print(file)
#         fs = FileSystemStorage()
#         # сохраняем на файловой системе
#         filename = fs.save(file.name, file)
#         # получение адреса по которому лежит файл
#         file_url = fs.url(filename)
#         return render(request, 'certs/get_new_certificate.html', {
#             'file_url': file_url
#         })
#
#     return render(request, 'certs/get_new_certificate.html')
#
#
# def certificate_done(request):
#     return render(request, 'certs/certificate_done.html')
#
#
# def get_certificates(request):
#     if request.method == 'POST' and request.FILES:
#         form = CertForm(request.POST, request.FILES)
#         files = request.FILES.getlist('files')
#         if form.is_valid():
#             id = form.save().pk
#             cert = Cerificate.objects.get(pk=id)
#             form.save()
#         # получаем загруженный файл
#         # new_files = request.FILES
#         # print(new_files)
#         # fs = FileSystemStorage()
#         # # сохраняем на файловой системе
#         # filename = fs.save(file.name, file)
#         # # получение адреса по которому лежит файл
#         # file_url = fs.url(filename)
#         # return render(request, 'certs/get_new_certificate.html', {
#         #     'file_url': file_url
#         # })
#             return HttpResponseRedirect("certificates")
#     else:
#         form = CertForm
#
#     return render(request, 'certs/get_certificates.html', {'form': form})
