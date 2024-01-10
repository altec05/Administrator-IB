from .models import Cerificate
from django.forms import ModelForm
from django import forms


class CertForm(forms.Form):
    # file_field = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    sn_field = forms.CharField(widget=forms.HiddenInput)


class CertAdminForm(forms.ModelForm):
    class Meta(object):
        model = Cerificate
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CertAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Since the pk is set this is not a new instance
            if self.instance.city != 'Красноярск':
                self.fields['testing'].widget = forms.HiddenInput()
