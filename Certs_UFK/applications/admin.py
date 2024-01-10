import datetime

from django.contrib import admin
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
    # def save_model(self, request, obj, form, change):
    #     obj.snils = obj.snils.replace('-', '').replace(' ', '')
    #     obj.save()
    #     if change:
    #         obj.passport_series = obj.worker.passport_series
    #         obj.passport_number = obj.worker.passport_number
    #         obj.passport_from_date = obj.worker.passport_from_date
    #         obj.passport_from_code = obj.worker.passport_from_code
    #         obj.date_of_birth = obj.worker.date_of_birth
    #         obj.place_of_birth = obj.worker.place_of_birth
    #         obj.gender = obj.worker.get_gender_display()
    #         obj.last_name = obj.worker.last_name
    #         obj.first_name = obj.worker.first_name
    #         obj.patronymic = obj.worker.patronymic
    #         obj.inn = obj.worker.inn
    #         obj.snils = obj.worker.snils
    #         obj.job = obj.worker.job
    #         obj.email = obj.worker.email
    #         obj.city_2 = obj.worker.get_city_display()
    #         obj.document_name = obj.worker.document_name
    #         obj.document_date = obj.worker.document_date
    #         obj.document_number = obj.worker.document_number
    #         obj.document_path = obj.worker.document_path
    #         obj.save()
    #     else:
    #         obj.tofk = obj.worker.tofk_number
    #         obj.city_1 = obj.worker.get_city_display()
    #         obj.passport_series = obj.worker.passport_series
    #         obj.passport_number = obj.worker.passport_number
    #         obj.passport_from_date = obj.worker.passport_from_date
    #         obj.passport_from_code = obj.worker.passport_from_code
    #         obj.date_of_birth = obj.worker.date_of_birth
    #         obj.place_of_birth = obj.worker.place_of_birth
    #         obj.gender = obj.worker.get_gender_display()
    #         obj.last_name = obj.worker.last_name
    #         obj.first_name = obj.worker.first_name
    #         obj.patronymic = obj.worker.patronymic
    #         obj.inn = obj.worker.inn
    #         obj.snils = obj.worker.snils
    #         obj.job = obj.worker.job
    #         obj.email = obj.worker.email
    #         obj.city_2 = obj.worker.get_city_display()
    #         obj.document_name = obj.worker.document_name
    #         obj.document_date = obj.worker.document_date
    #         obj.document_number = obj.worker.document_number
    #         obj.document_path = obj.worker.document_path
    #         obj.save()


class ApplicationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('city', 'a_type', 'subject', 'certificate_done',  'ap_formed', 'req_send', 'req_approved', 'cert_done', 'cert_get', 'updated_at', 'created_at')
    list_display_links = ('a_type','subject',)
    search_fields = ('subject', 'city',)
    list_filter = ('created_at', 'city', 'a_type', 'certificate_done', 'req_formed', 'doc_signed', 'ap_formed', 'ap_signed', 'req_send', 'req_approved', 'need_go', 'cert_done', 'cert_get', 'token_done', 'token_type', 'updated_at')
    readonly_fields = ['city', 'created_at', 'updated_at', 'certificate_done', 'doc_path', 'ap_path']
    autocomplete_fields = ['certificate', ]
    fields = [field.name for field in Application._meta.get_fields() if field.name != "id"]

    def get_form(self, request, obj=None, **kwargs):
        try:
            if obj.a_type == "reload":
                self.exclude = ("ap_sent", 'ap_signed', 'ap_path', 'req_approved', 'need_go', 'need_go_to', 'need_go_2', 'need_go_to_2', 'cert_done')
        except:
            pass
        form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
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