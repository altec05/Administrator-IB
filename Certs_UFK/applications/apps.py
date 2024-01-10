from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications'
    verbose_name = "Заявления на выпуск сертификата в УЦ ФК"
