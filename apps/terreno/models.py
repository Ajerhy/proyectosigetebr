from django.db import models
from apps.usuario.models import EstadoModel
from django.urls import reverse
from apps.usuario.templatetags.utils import PROCESO

class Ubicacion(EstadoModel):
    latitudubicacion = models.CharField(max_length=30, blank=True, null=True,
                                              verbose_name = 'Latitud',
                                              help_text = 'Ingrese la Latitud')
    longitudubicacion = models.CharField(max_length=30, blank=True, null=True,
                                              verbose_name = 'Longitud',
                                              help_text = 'Ingrese la Longitud')
    descripcionubicacion = models.CharField(max_length=50, blank=True, null=True,
                                              verbose_name = 'Descripcion de la Ubicacion',
                                              help_text = 'Ingrese Descripcion de la Ubicacion')
    def __str__(self):
        return '%s %s' % (self.latitudubicacion,self.longitudubicacion)

    class Meta:
        verbose_name_plural = "Ubicaciones"

class Medida(EstadoModel):
    largomedida = models.IntegerField(blank=True, null=True,verbose_name='Medida Largo del Lote')
    anchomedida = models.IntegerField(blank=True, null=True,verbose_name='Medida Ancho del Lote')
    superficietotal = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('terreno:detalle_medida', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s %s' % (self.largomedida, self.anchomedida)

    def __repr__(self):
        return self.largomedida

    class Meta:
        verbose_name_plural = "Medidas"
        ordering = ['creacion']

class Distrito(EstadoModel):
    numerodistrito = models.IntegerField(blank=True, null=True,
                                              verbose_name = 'Numero del Distrito',
                                              help_text = 'Ingrese el Numero del Distrito')
    nombredistrito = models.CharField(max_length=50, blank=True, null=True,
                                              verbose_name = 'Nombre Distrito',
                                              help_text = 'Ingrese del Nombre Distrito')
    sigladistrito = models.CharField(max_length=10, blank=True, null=True,
                                              verbose_name = 'Sigla del Distrito',
                                              help_text = 'Ingrese la Sigla del Distrito')

    def __str__(self):
        return '%s %s %s' % (self.numerodistrito,self.nombredistrito,self.sigladistrito)

    class Meta:
        verbose_name_plural = "Distritos"

class Manzano(EstadoModel):
    distritos = models.ForeignKey(Distrito, null=True, blank=False, on_delete=models.CASCADE)

    codigomanzano = models.CharField(max_length=80,null=True, blank=False,
                                     verbose_name='Codigo Manzano',
                                     help_text='Ingresa Codigo Manzano')
    numeromanzano = models.IntegerField(blank=True, null=True,
                                         verbose_name='Numero del Manzano',
                                         help_text='Ingrese el Numero del Manzano')
    siglamanzano = models.CharField(max_length=10, blank=True, null=True, default='',
                                     verbose_name='Sigla del Manzano',
                                     help_text='Ingrese la Sigla del Manzano')
    procesomanzano = models.CharField(max_length=20,choices=PROCESO,
                                        verbose_name='Proceso',
                                        help_text = 'Ingrese Proceso Manzano')

    #lotes = models.ManyToManyField(Lote, blank=True)


    def __str__(self):
        return '%s %s' % (self.numeromanzano, self.codigomanzano)

    def __unicode__(self):
        return (self.codigomanzano)

    class Meta:
        verbose_name_plural = "Manzanos"
        ordering = ['creacion']

class Lote(EstadoModel):
    manzanos = models.ForeignKey(Manzano, null=False, blank=False, on_delete=models.CASCADE)

    codigolote = models.CharField(max_length=80,null=True, blank=False,
                                     verbose_name='Codigo Lote',
                                     help_text='Ingresa Codigo Lote')
    numerolote = models.IntegerField(blank=True, null=True,
                                        verbose_name='Numero del Lote',
                                        help_text='Ingrese el Numero del Lote')
    siglalote = models.CharField(max_length=10, blank=True, null=True, default='',
                                     verbose_name='Sigla del Lote',
                                     help_text='Ingrese la Sigla del Lote')
    procesolote = models.CharField(max_length=20,choices=PROCESO,
                                        verbose_name='Proceso',
                                        help_text = 'Ingrese Proceso Lote')

    medidas = models.ForeignKey(Medida, null=True, blank=True, on_delete=models.CASCADE)

    ubicaciones = models.ForeignKey(Ubicacion, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.codigolote, self.manzanos.codigomanzano)

    def __unicode__(self):
        return (self.codigolote)

    class Meta:
        verbose_name_plural = "Lotes"
        ordering = ['creacion']
