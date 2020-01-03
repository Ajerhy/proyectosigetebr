from apps.terreno.models import Manzano
from django import forms

class ManzanoForm(forms.ModelForm):
    class Meta:
        model = Manzano
        fields = ['distritos',
                  'numeromanzano',
                  'procesomanzano']
        labels = {'distritos':"Ingrese el Distrito",
                  'numeromanzano': "Ingrese Numero Manzano",
                  'procesomanzano':"Estado del Manzano"
                  }
        widgets = {
            'numeromanzano': forms.NumberInput(),
            #'anchomedida': forms.TextInput(),
            #'descripcioncategoria': forms.Textarea()
                   }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })