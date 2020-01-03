from django import forms
from django.forms import ModelForm
from apps.contrato.models import Urbanizacion

class UrbanizacionForm(ModelForm):
    class Meta:
        model = Urbanizacion
        fields = ['nombreubanizacion',
                  'numeromatricula',
                  'ubicacion',
                  'propietaria',
                  'cuentas',
                  'logoubanizacion']
        labels = {'nombreubanizacion': 'Nombre Urbanizacion',
                  'numeromatricula': 'Numero Derechos Reales',
                  'ubicacion': 'Ubicacion',
                  'propietaria': 'Propietario',
                  'cuentas': 'Cuentas',
                  'logoubanizacion': 'Ingrese Logo Urbanizacion'}
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })