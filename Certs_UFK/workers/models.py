from django.db import models


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


# Данные сотрудника
class Worker(models.Model):
    city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    full_name = models.CharField(max_length=200, verbose_name='ФИО', blank=True, unique=True)
    job = models.CharField(max_length=200, verbose_name='Должность')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Отдел', blank=True, null=True)

    Gender_Choices = (
        ('male', 'М'),
        ('female', 'Ж'),
    )

    gender = models.CharField(max_length=6, choices=Gender_Choices, default=Gender_Choices[0], verbose_name='Пол')
    email = models.EmailField(max_length=200, verbose_name='Почта', blank=True)
    visibility = models.BooleanField(default=True, verbose_name='Видимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

    class Meta:
        ordering = ['city', 'last_name']
        # ordering = ['last_name',]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
