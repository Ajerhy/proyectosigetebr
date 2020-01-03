from django import forms
from django.forms import ModelForm
from apps.contrato.models import Persona
from apps.usuario.templatetags.utils import SEXOS, EXPEDIDOS

"""
Constantes
"""

ERROR_MESSAGE_CI = {'required':'El numero de cedula de identidad es requerido','unique':'El numero de cedula de identidad ya se encuentra registrado','invalid': 'Ingrese el numero de cedula de identidad valido'}
FORMATO_FECHA = ['%Y-%m-%d']

def get_ci(value_generopersona):
    if len(value_generopersona) < 6:
        raise forms.ValidationError('Numero de Cedula de Identidad debe tener mas de 6 Caracter')

class PersonaForm(ModelForm):
    nombrepersona = forms.CharField(max_length=50,label='Nombre')
    paternopersona = forms.CharField(max_length=90,label='Apellido Paterno',required=False)
    maternopersona = forms.CharField(max_length=90,label='Apellido Materno',required=False)
    cipersona = forms.CharField(max_length=20,label='Cedula de Identidad',validators = [get_ci])

    class Meta:
        model = Persona
        fields = ['nombrepersona','paternopersona','maternopersona',
                  'cipersona','expedidopersona','generopersona','nacimientopersona']

        labels = {'generopersona': 'Genero',
                  'nacimientopersona': 'Fecha de Nacimiento'}
        widgets = {
        'expedidopersona' : forms.Select(choices=EXPEDIDOS),
        'nacimientopersona' : forms.DateInput(attrs={'type': 'text'}),
        'generopersona': forms.Select(choices=SEXOS)
        }
#'type': 'date'
    def clean_cipersona(self):
        ci = self.cleaned_data['cipersona']
        persona = Persona.objects.filter(cipersona__iexact=ci).exclude(id=self.instance.id)
        if persona:
            raise forms.ValidationError("El Numero de Cedula de Identidad Ya Existe")
        else:
            return ci

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
