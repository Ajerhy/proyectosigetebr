from apps.terreno.models import Distrito
from django import forms

class DistritoForm(forms.ModelForm):
    class Meta:
        model = Distrito
        fields = ['numerodistrito',
                  'anchomedida',
                  'superficietotal']
        labels = {'numerodistrito':"Ingrese el Largo",
                  'nombredistrito': "Ingrese el Ancho",
                  'sigladistrito':"Medicion Superficie"
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