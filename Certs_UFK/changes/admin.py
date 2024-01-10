from django.contrib import admin
from .models import ChangeLog, Version


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'changes')
    list_filter = ('visibility',)
    readonly_fields = ('created_at', 'updated_at' )
    # fields = ('city', 'last_name', 'first_name', 'patronymic', 'full_name', 'job', 'department', 'gender', 'email', 'visibility',
    #           'created_at', 'updated_at')


class VersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'change_log', 'date_of_update')
    list_display_links = ('version',)
    search_fields = ('version', 'change_log__name', 'change_log__changes')
    list_filter = ('visibility',)
    # readonly_fields = ('created_at', 'updated_at' )


admin.site.register(Version, VersionAdmin)
admin.site.register(ChangeLog, ChangeLogAdmin)
