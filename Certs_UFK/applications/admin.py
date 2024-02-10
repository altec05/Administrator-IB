import datetime

from django.contrib import admin, messages

from workers.models import Worker
from certs.models import Cerificate
# from .models import Application, Subject
from .models import Application, TOFK, Subject


class TOFKAdmin(admin.ModelAdmin):
    list_display = ('tofk_number', 'tofk_city', 'tofk_address')
    list_display_links = ('tofk_number',)
    search_fields = ('tofk_number', 'tofk_address')
    fields = ('tofk_number', 'tofk_city', 'tofk_address')


class SubjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('city_1', 'worker', 'tofk_number', 'updated_at')
    list_display_links = ('city_1', 'worker',)
    search_fields = ()
    list_filter = ('city_1', 'tofk_number')
    # readonly_fields = [field.name for field in Subject._meta.get_fields() if field.name != "worker" if field.name != "note" if field.name != "id"]
    readonly_fields = ['help_text', 'created_at', 'updated_at', 'city_1', 'city_2', 'gender', 'last_name', 'first_name', 'patronymic', 'job']
    fields = ('help_text', 'worker', 'tofk_number', 'city_1', 'passport_path', 'passport_series', 'passport_number', 'passport_from', 'passport_from_date', 'passport_from_code', 'date_of_birth', 'place_of_birth', 'gender', 'last_name', 'first_name', 'patronymic', 'inn', 'snils', 'job', 'email', 'city_2', 'document_name', 'document_date', 'document_number', 'document_path', 'created_at', 'updated_at', 'note')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "worker":
            kwargs["queryset"] = Worker.objects.filter(visibility=True).order_by('last_name')
        return super(SubjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.snils:
            obj.snils = obj.snils.replace('-', '').replace(' ', '')
            obj.save()
        if change:
            obj.city_1 = obj.worker.get_city_display()
            obj.gender = obj.worker.get_gender_display()
            obj.last_name = obj.worker.last_name
            obj.first_name = obj.worker.first_name
            obj.patronymic = obj.worker.patronymic
            obj.job = obj.worker.job
            obj.city_2 = obj.worker.get_city_display()
            obj.save()
        else:
            obj.city_1 = obj.worker.get_city_display()
            obj.gender = obj.worker.get_gender_display()
            obj.last_name = obj.worker.last_name
            obj.first_name = obj.worker.first_name
            obj.patronymic = obj.worker.patronymic
            obj.job = obj.worker.job
            obj.city_2 = obj.worker.get_city_display()
            obj.save()


class ApplicationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('certificate_done', 'city', 'a_type', 'subject',  'ap_formed', 'req_send', 'req_approved', 'cert_get', 'cert_done', 'sign_done', 'updated_at', 'created_at')
    list_display_links = ('a_type','subject',)
    search_fields = ('subject__last_name', 'subject__first_name', 'subject__patronymic', 'city',)
    list_filter = ('created_at', 'city', 'a_type', 'certificate_done', 'req_formed', 'doc_signed', 'ap_formed', 'ap_signed', 'req_send', 'req_approved', 'need_go', 'cert_done', 'cert_get', 'token_done', 'token_type', 'updated_at')
    readonly_fields = ['city', 'created_at', 'updated_at', 'certificate_done', 'doc_path', 'ap_path']
    autocomplete_fields = ['certificate', ]
    fields = [field.name for field in Application._meta.get_fields() if field.name != "id"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.order_by('last_name')
        return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        from django import forms
        form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        try:
            if obj.a_type == "reload":
                form.base_fields["ap_sent"].widget = forms.HiddenInput()
                form.base_fields["ap_sent_data"].widget = forms.HiddenInput()
                form.base_fields["ap_signed"].widget = forms.HiddenInput()
                form.base_fields["ap_path"].widget = forms.HiddenInput()
                form.base_fields["req_approved"].widget = forms.HiddenInput()
                form.base_fields["need_go"].widget = forms.HiddenInput()
                form.base_fields["need_go_to"].widget = forms.HiddenInput()
                form.base_fields["need_go_2"].widget = forms.HiddenInput()
                form.base_fields["need_go_to_2"].widget = forms.HiddenInput()
                form.base_fields["cert_done"].widget = forms.HiddenInput()
                # self.exclude = ("ap_sent", 'ap_signed', 'ap_path', 'req_approved', 'need_go', 'need_go_to', 'need_go_2', 'need_go_to_2', 'cert_done')
        except:
            pass
        try:
            if obj.token_type == 'req':
                form.base_fields["token_sn"].widget = forms.HiddenInput()
        except:
            pass
        # if obj.token_type == 'req':
        #     print(obj.token_type, 123)
        #     try:
        #         self.fields.remove('token_sn')
        #     except:
        #         print('Нет такого поля уже!')
        #         pass
        # else:
        #     print('Поля:', self.fields)
        #     if not 'token_sn' in self.fields:
        #         print('1Нет поля sn!!!')
        #         self.fields.append('token_sn')
        #         print('1Добавили поле sn!!!')
        # if obj.token_type != 'req' and not 'token_sn' in self.fields:
        #     print('2Нет поля sn!!!')
        #     self.fields.append('token_sn')
        #     print('2Добавили поле sn!!!')
        # form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        try:
            if not obj.certificate and obj.cert_get:
                ln_subject = obj.subject.last_name
                id_subject = Worker.objects.get(last_name=ln_subject).pk
                obj.certificate = Cerificate.objects.get(subject=id_subject)
                if obj.certificate:
                    obj.cert_get = True
        except Exception as e:
            print(f'Ошибка: {e}')
            self.message_user(request=request, message=f'Сертификат для субъекта не найден!\nПо причине:\n{e}',
                              level=messages.WARNING)

        if obj.a_type != "reload":
            if obj.req_formed and obj.ap_formed and obj.ap_signed and obj.req_send and obj.req_approved and obj.need_go and obj.cert_done and obj.need_go_2 and obj.cert_get and obj.token_done and obj.sign_done:
                obj.certificate_done = True
                obj.save()
            else:
                obj.certificate_done = False
                obj.save()
        obj.city = obj.subject.city_1
        obj.ap_path = obj.subject.document_path
        obj.doc_path = obj.subject.document_path
        obj.save()




admin.site.register(TOFK, TOFKAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Application, ApplicationAdmin)