from django.contrib import admin
from .models import ChangeLog, Version


from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class StatusFilter(SimpleListFilter):
    title = _('Действующие списки')

    parameter_name = 'visibility_custom'

    def lookups(self, request, model_admin):
        return (
            (None, _('Все действующие')),
            ('True', _('Видимый')),
            ('False', _('Скрытый')),
            ('all', _('ВСЕ')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        print(self.value())
        if self.value() in ('True', 'False'):
            return queryset.filter(visibility=self.value())
        if self.value() == 'all':
            return queryset.filter()
        if self.value() is None:
            return queryset.filter(visibility='True')


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'changes')
    list_filter = (StatusFilter,)
    readonly_fields = ('created_at', 'updated_at' )
    # fields = ('city', 'last_name', 'first_name', 'patronymic', 'full_name', 'job', 'department', 'gender', 'email', 'visibility',
    #           'created_at', 'updated_at')


class VersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'change_log', 'date_of_update')
    list_display_links = ('version',)
    search_fields = ('version', 'change_log__name', 'change_log__changes')
    # readonly_fields = ('visibility',)
    list_filter = ('visibility',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "change_log":
            kwargs["queryset"] = ChangeLog.objects.filter(visibility=True).order_by('-created_at')
        return super(VersionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Version, VersionAdmin)
admin.site.register(ChangeLog, ChangeLogAdmin)
