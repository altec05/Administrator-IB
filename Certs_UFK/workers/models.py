from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


City_Choices = (
        ('achinsk', 'Ачинск'),
        ('kansk', 'Канск'),
        ('krasnoyarsk', 'Красноярск'),
        ('lesosibirsk', 'Лесосибирск'),
        ('minusinsk', 'Минусинск'),
        ('norilsk', 'Норильск'),
    )


# Отдел
class Department(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Название')
    short_name = models.CharField(max_length=200, verbose_name='Сокращение', unique=True)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ['short_name']
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


# # ТОФК
# class TOFK(models.Model):
#     tofk_number = models.CharField(max_length=4, verbose_name='Номер ТОФК', unique=True)
#     tofk_city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
#     tofk_address = models.CharField(max_length=255, verbose_name='Адрес ТОФК', unique=True)
#
#     def __str__(self):
#         return "%s - %s" % (self.tofk_number, self.get_tofk_city_display())
#
#     def clean(self):
#         if not str(self.tofk_number).isdigit():
#             raise ValidationError({'tofk_number': "ТОФК должен содержать только цифры!"})
#
#     class Meta:
#         ordering = ['tofk_number']
#         verbose_name = 'ТОФК'
#         verbose_name_plural = 'ТОФК'


# Данные сотрудника
class Worker(models.Model):
    city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    full_name = models.CharField(max_length=200, verbose_name='ФИО', blank=True, unique=True)
    job = models.CharField(max_length=200, verbose_name='Должность')
    # department = models.CharField(max_length=200, verbose_name='Отдел')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Отдел', blank=True, null=True)
    # inn = models.CharField(max_length=12, verbose_name='ИНН', validators=[MinLengthValidator(10)])
    # snils = models.CharField(max_length=14, verbose_name='СНИЛС', validators=[MinLengthValidator(11), MaxLengthValidator(14)])
    # passport_series = models.CharField(max_length=4, verbose_name='Серия паспорта', validators=[MinLengthValidator(4)])
    # passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта', validators=[MinLengthValidator(6)])
    # passport_from = models.CharField(max_length=200, verbose_name='Кем выдан')
    # passport_from_date = models.DateField(verbose_name='Когда выдан')
    # passport_from_code = models.CharField(max_length=7, verbose_name='Код места выдачи', validators=[MinLengthValidator(6)])
    # passport_path = models.CharField(max_length=255, verbose_name='Путь до паспорта', blank=True)

    Gender_Choices = (
        ('male', 'М'),
        ('female', 'Ж'),
    )

    gender = models.CharField(max_length=6, choices=Gender_Choices, default=Gender_Choices[0], verbose_name='Пол')
    # date_of_birth = models.DateField(verbose_name='Дата рождения')
    # place_of_birth = models.CharField(max_length=255, verbose_name='Место рождения')
    # tofk_number = models.ForeignKey(TOFK, on_delete=models.PROTECT, verbose_name='Номер ТОФК')
    email = models.EmailField(max_length=200, verbose_name='Почта', blank=True)
    # document_name = models.CharField(max_length=200, verbose_name='Название документа', blank=True)
    # document_date = models.DateField(verbose_name='Дата документа', blank=True, null=True)
    # document_number = models.CharField(max_length=200, verbose_name='Номер документа', blank=True)
    # document_path = models.CharField(max_length=255, verbose_name='Путь до документа', blank=True)
    visibility = models.BooleanField(default=True, verbose_name='Видимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

    # def clean(self):
    #     if not str(self.inn).isdigit():
    #         raise ValidationError({'inn': "ИНН должен содержать только цифры!"})
    #
    #     if not str(self.snils).isdigit():
    #         snils = str(self.snils).replace('-', '').replace(' ', '')
    #         self.snils = snils
    #         if not str(self.snils).isdigit():
    #             raise ValidationError({'snils': "СНИЛС должен содержать только цифры!"})
    #
    #     if not str(self.passport_series).isdigit():
    #         raise ValidationError({'passport_series': "Серия паспорта должна содержать только цифры!"})
    #
    #     if not str(self.passport_number).isdigit():
    #         raise ValidationError({'passport_number': "Номер паспорта должен содержать только цифры!"})
    #
    #     if not '-' in str(self.passport_from_code):
    #         raise ValidationError({'passport_from_code': "Код места выдачи паспорта должен содержать только цифры и"
    #                                                      " тире!"})
    #
    #     if not str(self.passport_from_code).isdigit():
    #         passport_from_code = str(self.passport_from_code).replace('-', '')
    #         if not passport_from_code.isdigit():
    #             raise ValidationError({'passport_from_code': "Код места выдачи паспорта должен содержать только цифры и"
    #                                                          " тире!"})

    class Meta:
        ordering = ['city', 'last_name']
        # ordering = ['last_name',]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


