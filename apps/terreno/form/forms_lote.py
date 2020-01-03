from apps.terreno.models import Lote
from django import forms

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['manzanos',
                  'codigolote',
                  'numerolote',
                  'siglalote',
                  'procesolote',
                  'medida',
                  'ubicacion',
                  ]
        labels = {'manzanos':"Ingrese el Manzano",
                  'codigolote': "Ingrese Codigo Lote",
                  'numerolote': "Ingrese Numero Lote",
                  'siglalote': "Ingrese Sigla del Lote",
                  'procesolote': "Estado Lote",
                  'medida': "Ingrese el Medida",
                  'ubicacion': "Ingrese el Ubicacion"
                  }
        widgets = {
            'manzanos': forms.TextInput(),
            'numerolote': forms.TextInput(),
            #'descripcioncategoria': forms.Textarea()
                   }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })