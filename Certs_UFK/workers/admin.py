from django.contrib import admin
# from .models import Worker, TOFK, Department
from .models import Worker, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'full_name')
    list_display_links = ('short_name',)
    search_fields = ('short_name', 'full_name')
    fields = ('short_name', 'full_name')


# class TOFKAdmin(admin.ModelAdmin):
#     list_display = ('tofk_number', 'tofk_city', 'tofk_address')
#     list_display_links = ('tofk_number',)
#     search_fields = ('tofk_number', 'tofk_address')
#     fields = ('tofk_number', 'tofk_city', 'tofk_address')


# class WorkerAdmin(admin.ModelAdmin):
#     list_display = ('city', 'last_name', 'first_name', 'patronymic', 'job', 'department', 'visibility', 'updated_at', 'created_at')
#     list_display_links = ('last_name',)
#     search_fields = ('last_name', 'job')
#     list_filter = ('city', 'department', 'job', 'visibility', 'gender')
#     readonly_fields = ('created_at', 'updated_at')
#     fields = ('city', 'last_name', 'first_name', 'patronymic', 'job', 'department', 'inn', 'snils', 'passport_series',
#               'passport_number', 'passport_from', 'passport_from_date', 'passport_from_code', 'passport_path', 'gender',
#               'date_of_birth', 'place_of_birth', 'tofk_number', 'email', 'document_name', 'document_date',
#               'document_number', 'document_path', 'visibility', 'created_at', 'updated_at')
#
#     def save_model(self, request, obj, form, change):
#         obj.snils = obj.snils.replace('-', '').replace(' ', '')
#         obj.save()


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('city', 'last_name', 'first_name', 'patronymic', 'job', 'department', 'visibility', 'updated_at',
                    'created_at')
    list_display_links = ('last_name',)
    search_fields = ('last_name', 'job')
    list_filter = ('city', 'department', 'job', 'visibility', 'gender')
    readonly_fields = ('created_at', 'updated_at' , 'full_name')
    fields = ('city', 'last_name', 'first_name', 'patronymic', 'full_name', 'job', 'department', 'gender', 'email', 'visibility',
              'created_at', 'updated_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            kwargs["queryset"] = Department.objects.order_by('short_name')
        return super(WorkerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.full_name = obj.last_name + ' ' + obj.first_name + ' ' + obj.patronymic
        obj.save()

admin.site.register(Worker, WorkerAdmin)
# admin.site.register(TOFK, TOFKAdmin)
admin.site.register(Department, DepartmentAdmin)