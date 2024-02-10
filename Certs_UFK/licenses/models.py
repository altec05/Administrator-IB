from django.db import models
import datetime
from django.core.exceptions import ValidationError

from workers.models import Worker, City_Choices


# Данные программы
class Program(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название ПО')
    version = models.CharField(max_length=255, verbose_name='Версия ПО', blank=True)
    soft_path = models.CharField(max_length=255, verbose_name='Путь до установочных файлов', blank=True)
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        out_str = ''
        if self.version:
            out_str = f'%s %s' % (self.name, self.version)
        else:
            out_str = f'%s' % (self.name,)
        return out_str

    class Meta:
        ordering = ['name', 'version']
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'


class Building(models.Model):
    city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
    street = models.CharField(max_length=250, verbose_name='Улица')
    building = models.CharField(max_length=250, verbose_name='Номер здания')

    def __str__(self):
        return f"%s, %s, %s" % (self.get_city_display(), self.street, self.building)

    class Meta:
        ordering = ['street']
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'


# Адрес установки
class Address(models.Model):
    city = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2], verbose_name='Город')
    building = models.ForeignKey(Building, on_delete=models.PROTECT, verbose_name='Здание')
    cabinet = models.CharField(max_length=255, verbose_name='Помещение', blank=True)
    inventory_number = models.CharField(max_length=255, verbose_name='Инвентарный номер', blank=True)
    note = models.TextField(verbose_name='Примечание', blank=True)

    def clean(self):
        if self.city and self.building:
            if not str(self.get_city_display()) in str(self.building):
                raise ValidationError({'city': "Город не совпадает с городом здания!"})

    def __str__(self):
        out_str = self.get_city_display()
        if self.cabinet:
            if not '.' in str(self.cabinet):
                if str(self.cabinet).isdigit():
                    out_str += f', каб. %s' % (self.cabinet,)
                else:
                    out_str += f', %s' % (self.cabinet,)
            else:
                out_str += f', %s' % (self.cabinet,)
        if self.inventory_number:
            if not 's/n' in str(self.inventory_number):
                out_str += f', инв. %s' % (self.inventory_number,)
            else:
                out_str += f', %s' % (self.inventory_number,)
        return out_str + f', {self.note}'


    class Meta:
        ordering = ['building', 'cabinet', 'inventory_number']
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


# Акт установки
class ActOfInstall(models.Model):
    date = models.DateField(verbose_name='Дата документа')
    address_of_install = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='Место установки')
    owner = models.ForeignKey(Worker, on_delete=models.PROTECT, verbose_name='Владелец')
    file = models.FileField(blank=True, upload_to='acts_of_install/')
    file_path = models.CharField(max_length=255, verbose_name='Путь до файла', blank=True, null=True)

    def __str__(self):
        return f"Акт от %s, %s" % (datetime.date.strftime(self.date, '%d.%m.%Y'), self.address_of_install)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Акт'
        verbose_name_plural = 'Акты'


# Данные лицензии
class License(models.Model):
    program = models.ForeignKey(Program, on_delete=models.PROTECT, verbose_name='Предмет лицензии')
    serial_number = models.CharField(max_length=255, verbose_name='Серийный номер', blank=True)
    lic_end = models.DateField(verbose_name='Срок действия лицензии', blank=True, null=True)
    amount = models.PositiveIntegerField(verbose_name='Шт.', blank=True, default=1)
    files_path = models.CharField(max_length=255, verbose_name='Место хранения', blank=True, help_text='Укажите файловую папку или физическое место хранения документа', default='ул. ПЖ, д. 3м, каб. 117, сейф, папка с лицензиями')
    date_of_receiving = models.DateField(verbose_name='Дата получения', blank=True, null=True)
    received_from = models.CharField(max_length=255, verbose_name='Получено от', blank=True)
    installed = models.BooleanField(default=False, verbose_name='Установлено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    note = models.TextField(verbose_name='Примечание', blank=True)

    def __str__(self):
        out_str = self.program.__str__()
        if self.amount:
            out_str += f', {self.amount} шт.'
        if self.serial_number:
            out_str += f', s/n - {self.serial_number}'
        return out_str

    def clean(self):
        if License.objects.filter(serial_number=self.serial_number):
            not_uniq = False
            for lic in License.objects.filter(serial_number=self.serial_number):
                if not lic == self:
                    if self.program == lic.program:
                        if self.amount:
                            if self.amount == lic.amount:
                                not_uniq = True
                        if self.date_of_receiving:
                            if self.date_of_receiving == lic.date_of_receiving:
                                not_uniq = True
                        if not self.amount and not self.date_of_receiving:
                            not_uniq = True
                    if not_uniq:
                        raise ValidationError(
                            {'serial_number': f'Запись с указанным серийным номером уже зарегистрирована! "{lic}"'})

    def city_installed(self):
        cities = []
        if Installation.objects.filter(lic=self):
            for install in Installation.objects.filter(lic=self):
                temp = install.city_of_install
                city = ''
                for row in City_Choices:
                    if temp in row:
                        city = row[row.index(temp) + 1]
                if city:
                    if not city in cities:
                        cities.append(city)
        return cities

    def places_installed(self):
        places = []
        if Installation.objects.filter(lic=self):
            for install in Installation.objects.filter(lic=self):
                temp = install.place
                if temp:
                    if not temp in places:
                        places.append(temp)
        return places

    def subjects_install(self):
        subjects = []
        if Installation.objects.filter(lic=self):
            for install in Installation.objects.filter(lic=self):
                subj = install.subject
                if subj:
                    if not subj in subjects:
                        subjects.append(subj)
        return subjects

    def total_left(self):
        left = self.amount
        for install in Installation.objects.filter(lic=self):
            left = left - install.count
        return left

    total_left.short_description = '*Свободно'
    city_installed.short_description = '*Город установки'
    places_installed.short_description = '*Место установки'
    subjects_install.short_description = '*Кому'

    class Meta:
        ordering = ['program', 'serial_number']
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'


class Installation(models.Model):
    lic = models.ForeignKey(License, on_delete=models.PROTECT, verbose_name='ПО')
    city_of_install = models.CharField(max_length=200, choices=City_Choices, default=City_Choices[2],
                                       verbose_name='Город')
    date_of_install = models.DateField(verbose_name='Дата установки', blank=True, null=True)
    place = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='Место установки', blank=True, null=True)
    subject = models.ForeignKey(Worker, on_delete=models.PROTECT, verbose_name='Владелец', blank=True, null=True)
    count = models.IntegerField(default=1, verbose_name='Использовано лицензий')

    def __str__(self):
        if self.date_of_install:
            return f"%s в %s на %s шт." % (datetime.date.strftime(self.date_of_install, '%d.%m.%Y'), self.get_city_of_install_display(), self.count)
        else:
            return f"%s на %s шт." % (self.get_city_of_install_display(), self.count)

    def clean(self):
        if self.city_of_install and self.place:
            if not str(self.get_city_of_install_display()) in str(self.place):
                raise ValidationError({'place': "Место установки не совпадает с городом установки!"})

    class Meta:
        ordering = ['-date_of_install']
        verbose_name = 'Установки'
        verbose_name_plural = 'Установки'


class InstallSoft(models.Model):
    install = models.ForeignKey(Installation, on_delete=models.PROTECT, verbose_name='Установка', blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, verbose_name='ПО', blank=True, null=True)
    distr_version = models.CharField(verbose_name='Версия дистрибутива', blank=True, max_length=25)

    def __str__(self):
        return f"%s %s" % (self.program, self.distr_version)

    class Meta:
        ordering = ['program']
        verbose_name = 'Установка ПО'
        verbose_name_plural = 'Установки ПО'
