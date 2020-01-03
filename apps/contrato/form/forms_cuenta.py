from django import forms
from apps.contrato.models import Cuenta
from django.forms import ModelForm

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['numerocuenta','banco','moneda']
        labels = {'numerocuenta': "Numero de Cuenta Bancaria",
                  "banco": "Nombre Banco",
                  "moneda": "Tipo de Moneda"}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_numerocuenta(self):
        numero = self.cleaned_data['numerocuenta']
        cuenta = Cuenta.objects.filter(numerocuenta__iexact=numero).exclude(id=self.instance.id)
        if cuenta:
            raise forms.ValidationError("El Numero de Cuenta Bancarria Ya esta Registrado")
        else:
            return numero
