from django import forms
from django.forms import ModelForm
from apps.contrato.models import Notaria

class NotariaForm(ModelForm):
    class Meta:
        model = Notaria
        fields = ['numeronotario', 'persona']
        labels = {'numeronotario': 'Numero Notario',
                  'persona': 'Ingrese Persona'}
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })