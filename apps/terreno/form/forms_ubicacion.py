from apps.terreno.models import Ubicacion
from django import forms

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['latitudubicacion',
                  'longitudubicacion',
                  'descripcionubicacion']
        labels = {'latitudubicacion':"Ingrese Latitud",
                  'longitudubicacion': "Ingrese Longitud",
                  'descripcionubicacion':"Descricion"
                  }
        widgets = {
            'latitudubicacion': forms.TextInput(),
            'longitudubicacion': forms.TextInput(),
            'descripcionubicacion': forms.Textarea()
                   }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })