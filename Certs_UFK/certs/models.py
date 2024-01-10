import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from workers.models import Worker, City_Choices
from django.utils.safestring import mark_safe
import os


# Метки для сертификата
class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        return f"%s" % (self.name,)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


# Данные о тестировании на допуск
class Testing(models.Model):
    subject = models.ForeignKey(Worker, on_delete=models.PROTECT, verbose_name='Субъект')
    year_of_birth = models.CharField(verbose_name='Год рождения', max_length=4, validators=[MinLengthValidator(4)])
    training = models.BooleanField(default=False, verbose_name='Тестирование')
    blank_number = models.CharField(max_length=255, verbose_name='Номер бланка тестирования', blank=True, null=True, default='ПОПЭП-', unique=True)
    training_date = models.DateField(verbose_name='Дата тестирования', blank=True, null=True)
    sign_doc = models.BooleanField(default=False, verbose_name='Ознакомление с Положением об ЭП')
    sign_doc_date = models.DateField(verbose_name='Дата ознакомления', blank=True, null=True)
    test_file = models.FileField(upload_to='education/tests/', verbose_name='Файл бланка тестирования', blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        try:
            return f"%s от %s" % (self.subject, datetime.date.strftime(self.training_date, '%d.%m.%Y'))
        except:
            return f"%s" % self.subject

    def clean(self):
        if self.training and self.training_date is None:
            raise ValidationError({'training_date': "Укажите Дату тестирования!"})

        if self.sign_doc and self.sign_doc_date is None:
            raise ValidationError({'sign_doc_date': "Укажите Дату ознакомления с Положением об ЭП!"})

        if self.training and not self.blank_number:
            raise ValidationError({'blank_number': "Укажите Номер бланка тестирования!"})

    class Meta:
        ordering = ['subject', 'blank_number']
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'


# Данные сертификата
class Cerificate(models.Model):
    cert_file = models.FileField(upload_to='certificates/', unique=True, verbose_name='Файл сертификата')
    city = models.CharField(max_length=255, verbose_name='Город', blank=True, null=True)
    subject = models.ForeignKey(Worker, on_delete=models.SET_NULL, verbose_name='Субъект', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Представление', blank=True, null=True)
    job = models.CharField(max_length=255, verbose_name='Должность', blank=True, null=True)
    serial_number = models.CharField(max_length=255, verbose_name='Серийный номер', blank=True, null=True)
    start_date = models.DateField(verbose_name='Дата создания', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)
    uc = models.CharField(max_length=255, verbose_name='УЦ', blank=True, null=True)
    snils = models.CharField(max_length=255, verbose_name='СНИЛС', blank=True, null=True)
    inn = models.CharField(max_length=255, verbose_name='ИНН', blank=True, null=True)
    ogrn = models.CharField(max_length=255, verbose_name='ОГРН', blank=True, null=True)
    tags = models.ManyToManyField(to=Tag, verbose_name='Метки', blank=True)
    tested = models.BooleanField(default=False, verbose_name='Тестирование')
    testing = models.ForeignKey(Testing, on_delete=models.PROTECT, verbose_name='Тестирование', blank=True, null=True)
    # training = models.BooleanField(default=False, verbose_name='Тестирование')
    # blank_number = models.CharField(max_length=255, verbose_name='Номер бланка тестирования', blank=True, null=True)
    # training_date = models.DateField(verbose_name='Дата тестирования', blank=True, null=True)
    # sign_doc = models.BooleanField(default=False, verbose_name='Положение')
    # sign_doc_date = models.DateField(verbose_name='Дата ознакомления', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        try:
            return f"%s, до %s" % (self.name, datetime.date.strftime(self.end_date, '%d.%m.%Y'))
        except:
            return f"%s, до %s" % (self.name, self.end_date)

    def tags_list(self):
        tags = []
        for tag in self.tags.all():
            if not tag.name in tags:
                tags.append(tag)
        return tags

    def fieldname_download(self):
        return mark_safe('<a href="/media/{0}" download>{1}</a>'.format(
            self.cert_file, self.cert_file))

    def clean(self):
        if self.subject and self.name:
            print(self.subject.full_name, self.name, self.subject.full_name != self.name, str(self.name).replace(' ', '').isalpha())
            if self.subject.full_name != self.name and str(self.name).replace(' ', '').isalpha():
                raise ValidationError(
                    {'subject': f'Выбранный сотрудник не соответствует сотруднику, указанному в сертификате!'})

    fieldname_download.allow_tags = True
    fieldname_download.short_description = 'Скачать сертификат'
    tags_list.short_description = '*Метки'


    # def clean(self):
    #     if self.training and self.training_date is None:
    #         raise ValidationError({'training_date': "Укажите Дату тестирования!"})
    #
    #     if self.sign_doc and self.sign_doc_date is None:
    #         raise ValidationError({'sign_doc_date': "Укажите Дату ознакомления с Положением об ЭП!"})
    #
    #     if self.training and not self.blank_number:
    #         raise ValidationError({'blank_number': "Укажите Номер бланка тестирования!"})

    class Meta:
        ordering = ['name', 'serial_number']
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
