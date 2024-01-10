import datetime
import os
from .forms import CertAdminForm
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from workers.models import Worker, City_Choices
from Certs_UFK.export_to_excel import export_certs
from .models import Tag, Cerificate, Testing
from .add_cert import get_cert
from .del_certs import del_old_certs
from Certs_UFK.forms import XlsxImportForm
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage


class TagAdmin(admin.ModelAdmin):
    save_on_top = False
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    # fields = [field.name for field in Program._meta.get_fields() if field.name != "id"]


class TestingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('subject', 'year_of_birth', 'training', 'blank_number', 'training_date')
    list_display_links = ('subject',)
    search_fields = ('subject', 'blank_number')
    list_filter = ('training', 'sign_doc', 'test_file')
    readonly_fields = ('created_at', 'updated_at')
    # fields = [field.name for field in Cerificate._meta.get_fields() if field.name != "id" if field.name != "application"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Worker.objects.order_by('last_name')
        return super(TestingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CertificateAdmin(admin.ModelAdmin):
    form = CertAdminForm
    save_on_top = True
    list_display = ('city', 'name', 'job', 'start_date', 'end_date', 'serial_number', 'tested', 'tags_list', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'job', 'serial_number', 'city', 'tags__name')
    list_filter = ('city', 'tags', 'job', 'tested')
    readonly_fields = ('fieldname_download', 'created_at', 'updated_at', 'name', 'job', 'start_date', 'end_date', 'uc', 'snils', 'inn', 'ogrn', 'city', 'tested')
    filter_horizontal = ('tags',)
    fields_temp = [field.name for field in Cerificate._meta.get_fields() if field.name != "id" if field.name != "application"]
    fields_temp.insert(0, 'fieldname_download')
    # fields = [ field.name for field in Cerificate._meta.get_fields() if field.name != "id" if field.name != "application"]
    fields = fields_temp
    change_list_template = 'certs/record_change_list.html'


    # def get_form(self, request, obj=None, **kwargs):
    #     try:
    #         if obj.city != "Красноярск":
    #             self.exclude = ("testing",)
    #     except:
    #         pass
    #     form = super(CertificateAdmin, self).get_form(request, obj, **kwargs)
    #     return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Worker.objects.order_by('last_name')
        return super(CertificateAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        urls = super().get_urls()
        # Добавляем URL нашего обработчика импорта.
        my_urls = [
            path('import-records-from-xlsx/', self.import_records_from_xlsx),
        ]
        return my_urls + urls

    def find_all(self, name, path):
        true_name = name.replace(' ', '_')
        result = []
        for root, dirs, files in os.walk(path):
            if true_name in files:
                result.append(os.path.join(root, true_name))
        return result

    def import_records_from_xlsx(self, request):
        context = admin.site.each_context(request)
        if request.method == 'POST':
            # Счетчик файлов, которые уже сохранены
            double_counter = 0
            # Счетчик истекших сертификатов
            old_counter = 0
            import_files = request.FILES.getlist('import_files')
            check_list = []
            clear_list = []
            counter_files = 0
            for file in import_files:
                counter_files += 1
                check_list.append(file)
                # check_list.append(file.name.replace(' ', '_'))
            folder = 'D:\PyProjects\Django\Certs_UFK\Certs_UFK\media\certificates'
            for file in check_list:
                name = file.name.replace(' ', '_')
                if not self.find_all(name, folder):
                    clear_list.append(file)
                else:
                    try:
                        print('!name!', name)
                        print('!name!!', 'certificates/' + name)
                        find_cert = Cerificate.objects.get(cert_file='certificates/' + name)
                        if find_cert:
                            print('!find_cert', find_cert)
                            double_counter += 1
                    except:
                        fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
                        name = file.name.replace(' ', '_')
                        filename = fs.delete(folder + r'\\' + name)
                        if not self.find_all(name, folder):
                            clear_list.append(file)

                    # self.message_user(request=request,
                    #                   message=f'Файл уже существует: {file.name}',
                    #                   level=messages.WARNING)

            if clear_list:
                for file in clear_list:
                    fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
                    name = file.name.replace(' ', '_')
                    filename = fs.save(name, file)

                records_to_save = []

                for file in clear_list:
                    data_to_save = {}
                    name = file.name.replace(' ', '_')
                    file_path = folder + r'\\' + name
                    data = get_cert(file_path)
                    # print('\ndata =\n', data, '\n')
                    data_to_save['name'] = data['name']
                    data_to_save['job'] = data['job']
                    data_to_save['serial_number'] = data['serial_number']
                    data_to_save['start'] = data['start']
                    data_to_save['stop'] = data['stop']
                    data_to_save['uc'] = data['uc']
                    data_to_save['snils'] = data['snils']
                    data_to_save['inn'] = data['inn']
                    data_to_save['ogrn'] = data['ogrn']
                    data_to_save['city'] = data['city']

                    if data['city'] and data['city'] == 'Красноярск':
                        if data.get('name'):
                            try:
                                id_worker = Worker.objects.get(full_name=data['name']).pk
                                data_to_save['testing'] = Testing.objects.get(subject=str(id_worker))
                            except:
                                last_name, first_name, patronymic = '', '', ''
                                if ' ' in data['name']:
                                    try:
                                        last_name, first_name, patronymic = data['name'].split(' ')
                                    except:
                                        last_name, first_name = data['name'].split(' ')
                                    worker = Worker(city=data['city'], last_name=last_name, first_name=first_name, patronymic=patronymic, full_name=data['name'], job=data['job'])
                                    try:
                                        worker.save()
                                    except Exception as e:
                                        self.message_user(request,
                                                          f'Работник не существует. Работник не создан: {data["name"]} - {e}.\n')

                                    self.message_user(request, f'Работник не существует. Создан работник!: {worker.id} {data["name"]}.\n')
                                else:
                                    self.message_user(request, f'Работник не существует. Создание отменено из-за некорректного имени: {data["name"]}\n')

                        if data_to_save.get('testing'):
                            data_to_save['tested'] = True
                        else:
                            data_to_save['tested'] = False
                    else:
                        data_to_save['tested'] = False
                        data_to_save['testing'] = None

                    fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
                    name = file.name.replace(' ', '_')
                    filename = fs.delete(folder + r'\\' + name)

                    if not data_to_save['stop'] < datetime.date.today():
                        new_obj = Cerificate(cert_file=file, city=data_to_save['city'], name=data_to_save['name'],
                                             job=data_to_save['job'], serial_number=data_to_save['serial_number'],
                                             start_date=data_to_save['start'], end_date=data_to_save['stop'],
                                             uc=data_to_save['uc'], snils=data_to_save['snils'],
                                             inn=data_to_save['inn'],
                                             ogrn=data_to_save['ogrn'], tested=data_to_save['tested'],
                                             testing=data_to_save.get('testing'))

                        records_to_save.append(new_obj)
                    else:
                        clear_list.remove(file)
                        old_counter += 1

                Cerificate.objects.bulk_create(records_to_save)
                output = ''
                counter = 0
                self.message_user(request, f'Импортировано строк: {len(records_to_save)}.\n{output}')
                if double_counter > 0:
                    self.message_user(request=request, message=f'Файлы уже существуют: {double_counter}', level=messages.WARNING)
                if old_counter > 0:
                    self.message_user(request=request, message=f'Срок действия уже истек: {old_counter}',
                                      level=messages.WARNING)
                for file in clear_list:
                    counter += 1
                    output += f'{counter}. ' + file.name + '\n'
                    self.message_user(request, f'{counter}. {file.name} \n')

            else:
                self.message_user(request, f'Список файлов, пригодных для импорта пуст!\nОбработано файлов: {counter_files}.')
                if double_counter > 0:
                    self.message_user(request=request, message=f'Файлы уже существуют: {double_counter}',
                                      level=messages.WARNING)
                if old_counter > 0:
                    self.message_user(request=request, message=f'Срок действия уже истек: {old_counter}',
                                      level=messages.WARNING)
            return redirect('/admin/certs/cerificate/')

        return render(request, 'certs/add_records_form.html', context=context)

    def save_model(self, request, obj, form, change):
        error_flag = False
        try:
            if request.FILES['cert_file']:
                files = request.FILES.getlist('cert_file')
                print('\nfiles =\n', files, '\n')
                if obj.cert_file:
                    print('\nobj.cert_file.name =\n', os.path.dirname(obj.cert_file.path), '\n')

                    if obj.cert_file:
                        folder = os.path.dirname(obj.cert_file.path)
                        name = os.path.basename(obj.cert_file.path)
                        # поиск файла в папке
                        if self.find_all(name, folder):
                            print('Файл уже в папке!!!')
                            error_flag = True
                        else:
                            error_flag = False
        except:
            pass

        if not error_flag:
            if form.is_valid():
                file = form.cleaned_data['cert_file']
                print('\nfile =\n', file, '\n')
                form.save()

            if obj.cert_file:
                if change or not obj.name:
                    cert_path = obj.cert_file.path
                    data = get_cert(cert_path)
                    # print('\ndata =\n', data, '\n')
                    obj.name = data['name']
                    obj.job = data['job']
                    obj.serial_number = data['serial_number']

                    obj.start_date = data['start']
                    obj.end_date = data['stop']
                    obj.uc = data['uc']
                    obj.snils = data['snils']
                    obj.inn = data['inn']
                    obj.ogrn = data['ogrn']
                    obj.city = data['city']
                if change:
                    if obj.testing:
                        obj.tested = True
                    else:
                        obj.tested = False
            try:
                if not obj.testing and obj.city == 'Красноярск':
                    print(obj.name)
                    id_worker = Worker.objects.get(full_name=obj.name).pk
                    print(id_worker)
                    obj.testing = Testing.objects.get(subject=str(id_worker))
                    print(obj.testing)
                    print(obj.name)

                    if obj.testing:
                        obj.tested = True
                    else:
                        obj.tested = False
            except Exception as e:
                print(f'Ошибка: {e}')
                self.message_user(request=request, message=f'Тестирование для работника не найдено!\nПо причине:\n{e}', level=messages.WARNING)

            # Если не установлен субъект, то ищем автоматически
            if not obj.subject:
                # Получаем ФИО из представления
                fio = obj.name.split(' ')
                last_name, first_name, patronymic = '', '', ''
                full_name = ''
                city = ''
                city_show = ''
                if fio:
                    if len(fio) == 3:
                        last_name, first_name, patronymic = fio
                        full_name = last_name + ' ' + first_name + ' ' + patronymic
                    else:
                        self.message_user(request=request, message=f'При создании сотрудника не удалось получить ФИО'
                                                                   f' нужного состава из {obj.name}!',
                                          level=messages.WARNING)
                else:
                    self.message_user(request, f'Не удалось получить ФИО из {obj.name}.\n')
                # Создаем работника для субъекта, если не существует или получаем его
                worker = ''
                if len(fio) == 3:
                    for row in City_Choices:
                        if obj.city in row:
                            city = City_Choices[City_Choices.index(row)][0]
                            city_show = City_Choices[City_Choices.index(row)][1]
                    try:
                        if obj.job:
                            worker, created = Worker.objects.update_or_create(last_name=last_name, first_name=first_name, patronymic=patronymic, full_name=full_name, job=obj.job, city=city)
                        else:
                            worker, created = Worker.objects.update_or_create(last_name=last_name, first_name=first_name, patronymic=patronymic, full_name=full_name, city=city)

                        # Если создали
                        if created:
                            self.message_user(request, message=mark_safe('Работник не существует. Создан работник: <a href="{0}">{1}</a> с данными: "{2}", "{3}", "М".'.format(reverse('admin:workers_worker_change', args=(worker.id,)), worker, city_show, obj.job)), level=messages.WARNING)
                    except Exception as e:
                        number = Worker.objects.filter(full_name=full_name).update(last_name=last_name, first_name=first_name,
                                                                          patronymic=patronymic, full_name=full_name,
                                                                          city=city, job=obj.job)
                        worker = Worker.objects.get(full_name=full_name)
                        if number:
                            if obj.job:
                                self.message_user(request, message=mark_safe('Работник <a href="{0}">{1}</a> обновлен данными из сертификата: "{2}", "{3}", "М". Ошибка поиска/создания: {4}!'.format(reverse('admin:workers_worker_change', args=(worker.id,)), worker, city_show, obj.job, e)))
                            else:
                                self.message_user(request, message=mark_safe('Работник <a href="{0}">{1}</a> обновлен данными из сертификата: "{2}", "М". Ошибка поиска/создания: {3}!'.format(reverse('admin:workers_worker_change', args=(worker.id,)), worker, city_show, e)))

                else:
                    try:
                        worker = Worker.objects.get(full_name=obj.name)
                    except:
                        self.message_user(request=request,
                                          message=f'Работник по сертификату {obj.name} не найден!',
                                          level=messages.WARNING)

                # Если нет субъекта и есть представление
                if worker:
                    if not obj.subject and obj.name:
                            obj.subject = worker
                else:
                    self.message_user(request=request,
                                      message=f'Операция присвоения субъекта для сертификата завершилась с ошибкой из-за ненахождения работника!',
                                      level=messages.WARNING)
            obj.save()
        else:
            print('cert_file= ', form.cleaned_data['cert_file'])
            # form.cleaned_data['cert_file'] = ''
            print('cert_file= ', form.cleaned_data['cert_file'])
            obj.cert_file = ''
            messages.set_level(request=request, level=messages.ERROR)
            self.message_user(request=request, message=f'Серийный номер для сертификата {form.cleaned_data["cert_file"]} уже зарегистрирован!', level=messages.ERROR)
            self.message_user(request=request, message='Загружаемый файл был удален!', level=messages.ERROR)
            obj.save()

    export_certs.short_description = "Выгрузка в Excel, XLSX"
    del_old_certs.short_description = 'Найти истекшие сертификаты из выбранных'

    actions = [export_certs, del_old_certs,]


admin.site.register(Tag, TagAdmin)
admin.site.register(Cerificate, CertificateAdmin)
admin.site.register(Testing, TestingAdmin)