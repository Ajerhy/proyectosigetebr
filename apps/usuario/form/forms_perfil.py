from apps.usuario.models import Perfil
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from apps.usuario.templatetags.utils import ROLES

"""
Funcion
"""

def must_be_gt(value_password):
    if len(value_password) < 7:
        raise forms.ValidationError('El Password debe tener mas de 8 Caracter')

"""
Constantes
"""

ERROR_MESSAGE_USUARIO = {'required':'El usuario es requerido','unique':'El usuario ya se encuentra registrado','invalid': 'Ingrese el usuario valido'}
ERROR_MESSAGE_PASSWORD = {'required':'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required':'el email es requerido','invalid':'Ingrese un correo valido'}

#Usuario Perfil Login
class LoginUsuarioPerfilForm(forms.ModelForm):
    usuario = forms.CharField(max_length= 15)
    password = forms.CharField(max_length= 15,widget=forms.PasswordInput)
    class Meta:
        model = Perfil
        fields = ['usuario', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginUsuarioPerfilForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError("¡La contraseña debe tener al menos 8 caracteres!")
        return password

    def clean(self):
        usuario = self.cleaned_data.get("usuario")
        password = self.cleaned_data.get("password")

        if usuario and password:
            self.perfil = authenticate(usuario=usuario,password=password)
            if self.perfil:
                if not self.perfil.estado:
                    pass
            else:
                pass
                #raise forms.ValidationError("Usuario y Contraseña no válidos")
        return self.cleaned_data

#Usuario Perfil Password
class PasswordUsuarioPerfilForm(forms.Form):
    password = forms.CharField( max_length= 20,label='Contraseña Actual', widget= forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Ingresa la Contraseña',
        'autocomplete': 'off'
        }) )
    new_password = forms.CharField(max_length=20,label='Nueva Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Ingresa la Contraseña',
        'autocomplete': 'off'
        }),validators = [must_be_gt] )
    repeat_password = forms.CharField( max_length= 20,label='Confirmar Nueva Contraseña', widget= forms.PasswordInput(attrs={
        'class': 'form-control',
        'type':'password',
        'placeholder': 'Ingresa Verificar Nueva Contraseña',
        'autocomplete': 'off'
        }),validators = [must_be_gt]  )

    def clean_repeat_password(self):
        clean_data = super(PasswordUsuarioPerfilForm,self).clean()
        password1 = clean_data['new_password']
        password2 = clean_data['repeat_password']
        if len(password1) < 8:
            raise forms.ValidationError(
                'La Contraseña debe tener al menos 8 Caracteres!')
        if password1 != password2:
            raise forms.ValidationError('La Confirmar Contraseña no coincide con la Nueva Contraseña')

#Usuario Perfil
class EditarUsuarioPerfilForm(forms.ModelForm):
    usuario = forms.CharField(max_length=20,label='Usuario',widget=forms.TextInput(
        attrs={'class': 'form-control',}),error_messages=ERROR_MESSAGE_USUARIO)
    email = forms.EmailField(label='Correo Electronico',
                            help_text='Ingresa Email',widget=forms.TextInput(attrs={
                'class': 'form-control',}),error_messages=ERROR_MESSAGE_EMAIL)
    nombre = forms.CharField(label='Nombre',max_length=50,
                                 help_text='Ingresa Nombre',widget=forms.TextInput(attrs={'class': 'form-control',}))
    apellido = forms.CharField(label='Apellidos', max_length=100,widget=forms.TextInput(attrs={
            'class': 'form-control',}),help_text='Ingresa Apellido',)

    class Meta:
        model = Perfil
        fields = ['usuario','email','roles','perfil_img']
        widgets = {'roles': forms.Select(choices=ROLES)}

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioPerfilForm, self).__init__(*args, **kwargs)

#Password-Reset
class PasswordResetEmailForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Perfil.objects.filter(email__iexact=email,estado=True).exists():
            raise forms.ValidationError("El Usuario no existe con este Correo Electrónico")
        return email

class PerfilFrom(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
