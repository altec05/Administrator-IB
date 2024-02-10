from django.contrib import admin
from .models import Program, Address, License, Installation, InstallSoft, Building
from workers.models import Worker
from Certs_UFK.export_to_excel import export_licens
import nested_admin


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'building')
    list_display_links = ('city',)
    list_filter = ('city',)


class ProgramAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'version')
    list_display_links = ('name',)
    search_fields = ('name', 'version',)
    # fields = [field.name for field in Program._meta.get_fields() if field.name != "id"]


class AddressAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('city', 'building', 'cabinet', 'inventory_number', 'note')
    list_display_links = ('building',)
    list_filter = ('city', 'building')
    search_fields = ('cabinet', 'inventory_number', 'note')
    # fields = [field.name for field in Address._meta.get_fields() if field.name != "id"]


class InstallInline(nested_admin.NestedTabularInline):
    model = InstallSoft
    extra = 0


class ActOfInstallAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('date', 'owner')
    list_display_links = ('date',)
    search_fields = ('owner',)
    autocomplete_fields = ['address_of_install',]
    readonly_fields = ['file_path']

    def save_model(self, request, obj, form, change):
        # Если нужно очистить файл, то удаляем
        try:
            print('\nCHECK =', request.POST['file-clear'])
            obj.file.delete()
            print('\nobj.file- =', obj.file)
            obj.save()
        except:
            pass
        # Если есть файл, то сохраняем его и путь к нему
        if obj.file:
            print('\nreq =', request.FILES)
            if not obj.file_path:
                obj.file_path = obj.file.path
                obj.save()
            else:
                if obj.file_path != obj.file.path:
                    obj.file_path = obj.file.path
                    obj.save()
        # Если нет файла, то очищаем путь
        else:
            if obj.file_path:
                obj.file_path = None
                obj.save()
                if obj.file_path:
                    print('\nobj.file_path =', obj.file_path)
            # Или просто сохраняем
            else:
                obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["queryset"] = Worker.objects.order_by('last_name')
        return super(ActOfInstallAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    # fields = [field.name for field in ActOfInstall._meta.get_fields() if field.name != "id"]


class LicenseInline(nested_admin.NestedStackedInline):
    model = Installation
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Worker.objects.order_by('last_name')
        return super(LicenseInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    autocomplete_fields = ['place']
    inlines = [InstallInline]


class LicenseAdmin(nested_admin.NestedModelAdmin):
    save_on_top = True
    list_display = ('program', 'serial_number', 'amount', 'total_left', 'date_of_receiving', 'installed', 'city_installed', 'places_installed', 'subjects_install', 'updated_at')
    list_display_links = ('program',)
    search_fields = ('program__name', 'program__version', 'serial_number', 'amount', 'files_path', 'received_from', 'installation__place__note', 'installation__place__inventory_number', 'installation__place__cabinet', 'installation__subject__full_name')
    list_filter = ('installed', 'installation__city_of_install', 'program__name')
    readonly_fields = ('created_at', 'updated_at', 'total_left')
    inlines = [LicenseInline]

    # filter_horizontal = ('place_of_install_address', 'act_of_install')

    # fields = [field.name for field in License._meta.get_fields() if field.name != "id" if field.name != "installation"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "program":
            kwargs["queryset"] = Program.objects.order_by('name')
        return super(LicenseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if Installation.objects.filter(lic=obj.pk):
                if not obj.installed:
                    obj.installed = True
            else:
                if obj.installed:
                    obj.installed = False
        obj.save()

    export_licens.short_description = "Выгрузка в Excel (.xlsx)"

    actions = [export_licens]


class InstallationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('lic', 'date_of_install', 'city_of_install', 'place', 'subject', 'count')
    list_display_links = ('lic',)
    search_fields = ('lic__program__name', 'lic__serial_number', 'place__city', 'place__cabinet', 'place__inventory_number', 'subject__last_name')
    list_filter = ('city_of_install',)

    inlines = [InstallInline]


class InstallAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('install', 'program', 'distr_version')
    search_fields = ('distr_version', 'program__name')


admin.site.register(Program, ProgramAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(InstallSoft, InstallAdmin)

