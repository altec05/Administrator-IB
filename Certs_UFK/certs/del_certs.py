import datetime
import os

from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from workers.models import Worker, City_Choices
from Certs_UFK.export_to_excel import export_certs
from .models import Tag, Cerificate, Testing
from .add_cert import get_cert
from Certs_UFK.forms import XlsxImportForm
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage


def del_old_certs(modeladmin, request, queryset):
    counter = 0
    for obj in queryset:
        if obj.end_date < datetime.date.today():
            print(obj, obj.end_date)
            cert = Cerificate.objects.get(id=obj.pk)
            print(cert)
            cert.delete()
            counter += 1
            messages.add_message(request, messages.INFO, f'Удален {cert}.')
    if counter == 0:
        messages.add_message(request, messages.INFO, f'Все сертификаты валидны!')

    return redirect('/admin/certs/cerificate/')
