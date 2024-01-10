from django.db import models
import datetime

from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


# Данные сотрудника
class ChangeLog(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок')
    changes = models.TextField(verbose_name='Список изменений')
    visibility = models.BooleanField(default=True, verbose_name='Видимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    def __str__(self):
        return "%s от %s" % (self.name, datetime.date.strftime(self.created_at, '%d.%m.%Y'))

    class Meta:
        ordering = ['-created_at', 'name']
        verbose_name = 'Список изменений'
        verbose_name_plural = 'Списки изменений'


# Версия проекта
class Version(models.Model):
    version = models.CharField(max_length=200, verbose_name='Версия проекта', unique=True)
    change_log = models.ForeignKey(ChangeLog, on_delete=models.PROTECT, verbose_name='Список изменений в версии')
    date_of_update = models.DateField(verbose_name='Дата обновления')
    visibility = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return "%s от %s" % (self.version, datetime.date.strftime(self.date_of_update, '%d.%m.%Y'))

    class Meta:
        ordering = ['-date_of_update']
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
