from django import forms
from django.forms import ModelForm
from apps.contrato.models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['persona',
                  'grupo',
                  'emailcliente',
                  'residenciacliente']
        labels = {'persona': 'Persona',
                  'grupo': 'Grupo',
                  'emailcliente': 'Email',
                  'residenciacliente': 'Direccion'}
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

"""
    model = Cliente
    fields = ['nombregrupo', 'descripciongrupo']

    labels = {'nombregrupo': 'Grupo',
              'descripciongrupo': 'Descripcion del Grupo'}
    widgets = {}
"""