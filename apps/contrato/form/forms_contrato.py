from django import forms
from django.forms import ModelForm
from apps.contrato.models import Contrato

class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ['cliente', 'lotes','tipopago']
        labels = {'cliente': 'Ingrese Cliente',
                  'lotes': 'Ingrese Lote',
                  'tipopago': 'Ingrese Tipo Pago'}
        #widgets = {}

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