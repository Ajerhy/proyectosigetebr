from django.db import models
from apps.usuario.models import EstadoModel
from django.core.validators import RegexValidator
from apps.terreno.models import Lote
from apps.terreno.models import Ubicacion
from apps.usuario.templatetags.utils import SEXOS,EXPEDIDOS,TIPOPAGO,PROPIETARIO

class Persona(EstadoModel):
    nombrepersona = models.CharField(max_length=100, blank=True, null=True,verbose_name='Nombre',
                                     help_text='Ingrese su Nombre')
    paternopersona = models.CharField(max_length=100, blank=True, null=True,verbose_name='Apellido Paterno',
                                      help_text = 'Ingrese su Apellido Paterno')
    maternopersona = models.CharField(max_length=100, blank=True, null=True,
                                      verbose_name='Apellido Materno',
                                      help_text='Ingrese su Apellido Materno')
    cipersona = models.CharField(max_length=20, blank=False, null=True,unique=True,#cambiar esta obligatorio numero carnet cliente
                                 verbose_name='Cedula de Identidad',
                                 help_text = 'Ingrese su Numero de Cedula de Identidad')
    expedidopersona = models.CharField(max_length=20,choices=EXPEDIDOS,blank=True,
                                        verbose_name='Expedido',
                                        help_text = 'Ingrese Expedido Ci')
    nacimientopersona = models.DateField(blank=True,null=True,
                                         verbose_name = 'Fecha de nacimiento',
                                         help_text = 'Seleccione su fecha de nacimiento')

    generopersona = models.BooleanField(default=1,choices=SEXOS,
                                        verbose_name='Genero',
                                        help_text = 'Ingrese Genero')
    def __str__(self):
        return '%s %s %s %s' % (self.cipersona,self.nombrepersona,self.paternopersona,self.maternopersona)

#    def save(self):
#        self.nombrepersona = self.nombrepersona.title()
#        self.paternopersona =self.paternopersona.title()
#        self.maternopersona = self.maternopersona.title()
#        super(Persona, self).save()

    class Meta:
        verbose_name_plural = "Personas"
        ordering = ['creacion']

class Grupo(EstadoModel):
    nombregrupo = models.CharField(max_length=30, blank=True, null=True)
    descripciongrupo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.nombregrupo)

    class Meta:
        verbose_name_plural = "Grupos"

class Cliente(EstadoModel):
    persona = models.ForeignKey(Persona, null=True,blank=True,on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.CASCADE)
    emailcliente = models.CharField(max_length=50, blank=True, null=True,
                                    verbose_name='Correo Electronico',
                                    help_text='Ingrese Email')
    residenciacliente = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.persona,self.grupo)

    class Meta:
        verbose_name_plural = "Clientes"
        ordering = ['creacion']

class Referenciacelular(EstadoModel):
    cliente = models.ForeignKey(Cliente, null=True,blank=True,on_delete=models.CASCADE)
    numeroreferenciacelular = models.CharField(max_length=50, blank=True, null=True,
                                    verbose_name='Numero Celular',
                                    help_text='Ingrese Numero Celular')
    def __str__(self):
        return (self.numeroreferenciacelular)

    class Meta:
        verbose_name_plural = "Referencia Celulares"
        ordering = ['creacion']

class Moneda(EstadoModel):
    nombremoneda = models.CharField(max_length=20, blank=True, null=True,
                                    verbose_name='Moneda',help_text='Ingrese el Nombre de la Moneda')
    siglamoneda = models.CharField(max_length=20, blank=True, null=True,
                                   verbose_name='Sigla de la Moneda',help_text='Ingrese la Sigla de la Moneda')
    detallemoneda = models.TextField(blank=True, null=True,
                                         verbose_name='Detalle de la Moneda',help_text='Ingrese el Detalle de la Moneda')
    def __str__(self):
        return '%s' % (self.siglamoneda)

    class Meta:
        verbose_name_plural = "Monedas"
        ordering = ['-creacion']

class Banco(EstadoModel):
    nombrebanco = models.CharField(max_length=50, blank=False, null=True,
                                     verbose_name='Nombre Banco',
                                     help_text='Ingrese su Nombre Banco')
    siglabanco = models.CharField(max_length=15, blank=True, null=True,
                                     verbose_name='Sigla Banco',
                                     help_text='Ingrese la Sigla Banco')
    def __str__(self):
        return '%s' % (self.nombrebanco)

    class Meta:
        verbose_name_plural = "Bancos"
        ordering = ['-creacion']

class Cuenta(EstadoModel):
    banco = models.ForeignKey(Banco, null=False, blank=True, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, null=False, blank=True, on_delete=models.CASCADE)
    numerocuenta = models.CharField(max_length=60, blank=False, null=False,unique=True,
                                     verbose_name='Numero de Cuenta Banco',
                                     help_text='Ingrese Numero de Cuenta Banco')


    def __str__(self):
        return '%s' % (self.numerocuenta)

    class Meta:
        verbose_name_plural = "Cuenta"
        ordering = ['-creacion']

class Notaria(EstadoModel):
    numeronotario = models.CharField(max_length=60, blank=False, null=False, unique=True,
                                    verbose_name='Numero de Notaria',
                                    help_text='Ingrese Numero de Notaria')
    persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.numeronotario,self.persona)

    class Meta:
        verbose_name_plural = "Notaria de Fe Publica"
        ordering = ['creacion']

class Propietaria(EstadoModel):
    #representante
    #apoderado
    persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=50, blank=True, null=True,
                                         verbose_name='Nombre Actividad',
                                         help_text='Ingrese del Nombre Actividad')
    tipo = models.CharField(max_length=20,choices=PROPIETARIO,blank=True,
                                        verbose_name='Tipo Propietario',
                                        help_text = 'Propietario')

#    copropietaria = models.ForeignKey('self', verbose_name=(u"Propietaria"),
#                                   help_text='Ingrese Propietaria',
#                                   related_name="propietaria_copropietaria", null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % (self.persona)

    class Meta:
        verbose_name_plural = "Propietaria"
        ordering = ['creacion']


class Urbanizacion(EstadoModel):
    nombreubanizacion = models.CharField(max_length=50, blank=True, null=True,
                                         verbose_name='Nombre Urbanizacion',
                                         help_text='Ingrese del Nombre Urbanizacion')
    numeromatricula = models.CharField(max_length=50, blank=True, null=True,
                                         verbose_name='Numero Matricula',
                                         help_text='Ingrese Numero Matricula de Urbanizacion')
    ubicacion = models.OneToOneField(Ubicacion, null=True, blank=True, unique=True, on_delete=models.CASCADE)
    propietaria = models.ForeignKey(Propietaria, null=True, blank=True, on_delete=models.CASCADE)
    cuentas = models.ManyToManyField(Cuenta, blank=True)
    logoubanizacion = models.ImageField(upload_to='static/photos/', null=True, blank=True)  # faltacorregir

    def __str__(self):
        return '%s' % (self.nombreubanizacion)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Urbanizacion"
        ordering = ['creacion']


class Contrato(EstadoModel):
    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)
    lotes = models.ManyToManyField(Lote, blank=True)
    tipopago = models.CharField(max_length=20,choices=TIPOPAGO,
                                        verbose_name='Pago',
                                        help_text = 'Ingrese Tipo Pago')

    def __str__(self):
        return '%s %s' % (self.cliente,self.tipopago)

    class Meta:
        verbose_name_plural = "Contratos"
        ordering = ['creacion']
