from django import forms
from django.forms import ModelForm
from apps.contrato.models import Referenciacelular

class MovilForm(forms.ModelForm):
    class Meta:
        model = Referenciacelular
        fields = ['cliente', 'numeroreferenciacelular']
        labels = {'cliente': 'Cliente',
                  'numeroreferenciacelular': 'Numero Telefono'}
        widgets = {}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })