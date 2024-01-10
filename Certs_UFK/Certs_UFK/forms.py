from django import forms
from Certs_UFK.settings import BASE_DIR
from workers.models import Worker


class GetPathForm(forms.Form):
    path = forms.FileField(required=True)


class PickWorkerForm(forms.Form):
    all_workers = Worker.objects.filter(visibility=True).order_by('full_name')
    workers = []
    for worker in all_workers:
        workers.append((worker.id, worker.full_name))

    worker_choice = forms.ChoiceField(choices=workers, label='Сотрудник', required=True)

    class Meta:
        widgets = {
            'worker_choice': forms.Select(attrs={'class': 'form-select form-control'}),
        }


class XlsxImportForm(forms.Form):
    import_folder_path = forms.CharField(help_text='Укажите путь до папки с импортируемыми сертификатами')