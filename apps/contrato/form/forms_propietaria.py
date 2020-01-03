from django import forms
from django.forms import ModelForm
from apps.contrato.models import Propietaria
class PropietariaForm(ModelForm):
    class Meta:
        model = Propietaria
        fields = ['persona', 'actividad']
        labels = {'persona': 'Ingrese Persona',
                  'actividad': 'Descripcion Activida Realiza'}
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })