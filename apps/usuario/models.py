from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin#, User
from django.utils import timezone
from apps.usuario.templatetags.utils import ROLES
import time
import uuid

class UserManager(BaseUserManager):
    def create_user(self, usuario, email, password):
        if not email:
            raise ValueError('El Email o Correo Electronico  es obligatorio')
        user = self.model(email=self.normalize_email(email))
        user.usuario = usuario
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email, password):
        user = self.create_user(usuario, email, password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("media", hash_, filename)

class EstadoModel(models.Model):
    #id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True, null=False, blank=False,editable=False)
    descripcion = models.TextField('descripcion', blank=True, null=True)
    direccion_ip = models.GenericIPAddressField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    estado = models.BooleanField(default=True)
    #uc = models.CharField(max_length=100, blank=True,null=True)
    #uc = models.ForeignKey(Usuario,blank=True,null=True,on_delete=models.CASCADE)#usuario creo
    uc = models.IntegerField(blank=True, null=True)
    #um =models.ForeignKey(User,on_delete=models.CASCADE)#usuario modifico
    #um = models.CharField(max_length=100, blank=True,null=True)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract = True

class Usuario(AbstractBaseUser, PermissionsMixin):
    #id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True, null=False, blank=False,editable=False)
    usuario = models.CharField('Usuario', max_length=15, unique=True)
    email = models.EmailField('Correo Electronico',max_length=50,unique=True)
    observacion = models.TextField(blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email',]

    def get_short_name(self):
        return self.usuario

    def get_full_name(self):
        return (self.usuario)

    def has_perm(self, perm, obj=None):
        "¿El usuario cuenta con los permisos en especificos?"
        return True

    def has_module_perms(self, app_label):
        "¿El usuario cuenta con los permisos para ver una app en especificos?"
        return True

    def __unicode__(self):
        return "%s" % (self.usuario)
#        return "%s %s" % (self.usuario, self.apellido)

    def __str__(self):
        return "%s" % (self.usuario)
#        return "%s %s" % (self.usuario, self.apellido)

    class Meta:
        ordering = ['-is_active']
        verbose_name_plural = "Usuarios"

#Perfil sera el Login Usuario SIGETEBR
class Perfil(Usuario):
    roles = models.CharField(max_length=20, choices=ROLES, default='Usuario')
    nombre = models.CharField('Nombres', max_length=50)
    apellido = models.CharField('Apellidos', max_length=50)
    phone = models.IntegerField(null=True,blank=True,help_text='Teléfono de contacto')
    perfil_img = models.ImageField(verbose_name='Imagen de Perfil',upload_to=img_url, blank=True, null=True)

    direccion_ip = models.GenericIPAddressField(blank=True, null=True)
    estado = models.BooleanField(default=True) #uc = models.ForeignKey(Usuario,on_delete=models.CASCADE)#usuario creo
    modificacion = models.DateTimeField(auto_now=True)  # , blank=True, null=True)
    uc = models.IntegerField(blank=True,null=True)
    um = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return '%s' % (self.usuario)

    class Meta:
        verbose_name_plural = "Perfiles"
