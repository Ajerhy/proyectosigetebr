from django import forms
from django.forms import ModelForm
from apps.contrato.models import Grupo

class GrupoForm(ModelForm):
    model = Grupo
    fields = ['nombregrupo', 'descripciongrupo']

    labels = {'nombregrupo': 'Grupo',
              'descripciongrupo': 'Descripcion del Grupo'}
    widgets = {}