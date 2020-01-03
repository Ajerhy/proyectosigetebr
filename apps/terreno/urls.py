from django.urls import path

#Ubicacion
from apps.terreno.view.views_ubicacion import UbicacionListarView
from apps.contrato.view.views_persona import PersonaListarView,PersonaCrearView,PersonaEditarView,PersonaDetalleView,\
    PersonaEliminarView,personadesactivar,personaactivar,cambiar_estado_persona

#Distrito
from apps.terreno.view.views_distrito import DistritoListarView

#Lote
from apps.terreno.view.views_lote import LoteListarView

#Manzano
from apps.terreno.view.views_manzano import ManzanoListarView

#Medida
from apps.terreno.view.views_medida import MedidaListarView,MedidaCrearView,MedidaEditarView,MedidaDetalleView,\
    MedidaEliminarView,medidadesactivar,medidaactivar,cambiar_estado_medida

app_name = 'terreno'
#int uuid
urlpatterns = [
    #Ubicacion
    path('listar/ubicacion/', UbicacionListarView.as_view(), name='listar_ubicacion'),
    path('crear/ubicacion/', PersonaCrearView.as_view(), name='crear_ubicacion'),
    path('editar/<int:pk>/ubicacion/', PersonaEditarView.as_view(), name='editar_ubicacion'),
    path('detalle/<int:pk>/ubicacion/', PersonaDetalleView.as_view(), name='detalle_ubicacion'),
    path('eliminar/<int:pk>/ubicacion/', PersonaEliminarView.as_view(), name='eliminar_ubicacion'),
    #
    path('desactivar/<int:id>/ubicacion/', personadesactivar, name='desactivar_ubicacion'),
    path('activar/<int:id>/ubicacion/', personaactivar, name='activar_ubicacion'),
    ##rapido
    path('estado/<int:pk>/ubicacion/', cambiar_estado_persona, name='estado_ubicacion'),
    #

    #Distrito
    path('listar/distrito/', DistritoListarView.as_view(), name='listar_distrito'),

    #Lote
    path('listar/lote/', LoteListarView.as_view(), name='listar_lote'),

    #Manzano
    path('listar/manzano/', ManzanoListarView.as_view(), name='listar_manzano'),


    #Medida
    path('listar/medida/', MedidaListarView.as_view(), name='listar_medida'),
    path('crear/medida/', MedidaCrearView.as_view(), name='crear_medida'),
    path('editar/<int:pk>/medida/', MedidaEditarView.as_view(), name='editar_medida'),
    path('eliminar/<int:pk>/medida/', MedidaEliminarView.as_view(), name='eliminar_medida'),
    path('detalle/<int:pk>/medida', MedidaDetalleView.as_view(), name='detalle_medida'),
    #
    path('desactivar/<int:id>/medida/', medidadesactivar, name='desactivar_medida'),
    path('activar/<int:id>/medida/', medidaactivar, name='activar_medida'),
    ##rapido
    path('estado/<int:pk>/medida/', cambiar_estado_medida, name='estado_medida'),
    #
]
