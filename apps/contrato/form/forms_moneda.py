from django import forms
from apps.contrato.models import Moneda
from django.forms import ModelForm

"""
Constantes
"""

class MoneyForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['nombremoneda', 'siglamoneda']
        widget = {'nombremoneda': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['nombremoneda', 'siglamoneda','detallemoneda']
        labels = {'nombremoneda': "Nombre Moneda",
                  "siglamoneda": "Sigla Moneda",
                  "detallemoneda": "Detalle Moneda"}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

"""
class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ('nombremoneda','siglamoneda','detallemoneda')
        widgets = {'nombremoneda': forms.TextInput(attrs={'class': 'form-control'}),
                   'siglamoneda': forms.TextInput(attrs={'class': 'form-control'}),
                   'detallemoneda': forms.TextInput(attrs={'class': 'form-control'})}
"""