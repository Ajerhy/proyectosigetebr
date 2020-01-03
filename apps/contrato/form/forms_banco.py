from django import forms
from apps.contrato.models import Banco
from django.forms import ModelForm

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombrebanco', 'siglabanco','descripcion']
        labels = {'nombrebanco': "Nombre Banco",
                  "siglabanco": "Sigla Banco",
                  "descripcion": "Descripcion Banco"}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
