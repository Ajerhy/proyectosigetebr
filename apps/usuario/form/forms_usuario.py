from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from apps.usuario.models import Usuario,Perfil
from django.utils import timezone


"""
Constantes
"""
ERROR_MESSAGE_USUARIO = {'required':'El usuario es requerido','unique':'El usuario ya se encuentra registrado','invalid': 'Ingrese el usuario valido'}
ERROR_MESSAGE_PASSWORD = {'required':'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required':'el email es requerido','invalid':'Ingrese un correo valido'}
"""
Funcion
"""

def must_be_gt(value_password):
    if len(value_password) < 7:
        raise forms.ValidationError('El Password debe tener mas de 8 Caracter')

def must_a_gt(value_password):
    if len(value_password) < 8:
        raise forms.ValidationError('El Password debe Caracteres Validos')
"""
Clases 
"""

#Login
class LoginUsuarioForm(forms.ModelForm):
    usuario = forms.CharField(max_length= 15)
    password = forms.CharField(max_length= 15,widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['usuario', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginUsuarioForm, self).__init__(*args, **kwargs)

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
            self.user = authenticate(usuario=usuario, password=password)
            if self.user:
                if not self.user.is_active:
                    pass
                    #raise forms.ValidationError("El usuario esta Inactivo")
            else:
                pass
                #raise forms.ValidationError("Usuario y Contraseña no válidos")
        return self.cleaned_data

#Usuario Password
class ActualizarPasswordForm(forms.Form):
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
        clean_data = super(ActualizarPasswordForm,self).clean()
        password1 = clean_data['new_password']
        password2 = clean_data['repeat_password']
        if len(password1) < 8:
            raise forms.ValidationError(
                'La Contraseña debe tener al menos 8 Caracteres!')
        if password1 != password2:
            raise forms.ValidationError('La Confirmar Contraseña no coincide con la Nueva Contraseña')

#Password-Reset
class PasswordResetEmailForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Usuario.objects.filter(email__iexact=email,is_active=True).exists():
            raise forms.ValidationError("El Usuario no existe con este Correo Electrónico")
        return email

#Usuario
class ActualizarUsuarioForm(forms.ModelForm):
    usuario = forms.CharField(max_length=20,label='Usuario',widget=forms.TextInput(
        attrs={'class': 'form-control',}),error_messages=ERROR_MESSAGE_USUARIO)
    email = forms.EmailField(label='Correo Electronico',
                            help_text='Ingresa Email',widget=forms.TextInput(attrs={
                'class': 'form-control',}),error_messages=ERROR_MESSAGE_EMAIL)
    class Meta:
        model = Usuario
        fields = ['usuario','email']
    def __init__(self, *args, **kwargs):
        super(ActualizarUsuarioForm, self).__init__(*args, **kwargs)


class UsuarioForm(forms.ModelForm):
    usuario = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USUARIO)
    email = forms.EmailField(error_messages=ERROR_MESSAGE_EMAIL)
    #nombre = forms.CharField(max_length=50)
    #apellido = forms.CharField(max_length=100)
    #perfil_pic = forms.FileInput()

    class Meta:
        model = Usuario
        fields = ['usuario', 'email', 'observacion']
        labels = {'usuario': "Usuario",
                  'email': "Email",
                  'observacion': "Observacion"}
        widgets = {'observaciones': forms.Textarea(attrs={
            'cols': 10, 'rows': 5,'placeholder': 'Ingrese detalle Observacion',
                'class': 'border border-info'})}

        #widgets = {'publication_date': forms.DateInput(attrs={'type': 'date'})}
        #widget = {'perfil_pic': forms.FileInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

