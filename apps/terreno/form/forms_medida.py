from apps.terreno.models import Medida
from django import forms

class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ['largomedida',
                  'anchomedida',
                  'superficietotal']
        labels = {'Largo':"Ingrese el Largo",
                  'Ancho': "Ingrese el Ancho",
                  'Superficie':"Medicion Superficie"
                  }
        widgets = {
            'largomedida': forms.TextInput(),
            'anchomedida': forms.TextInput(),
            #'descripcioncategoria': forms.Textarea()
                   }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })