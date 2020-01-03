from django.urls import path

#Persona
from apps.contrato.view.views_persona import PersonaListarView,PersonaCrearView,PersonaEditarView,PersonaDetalleView,\
    PersonaEliminarView,personadesactivar,personaactivar,cambiar_estado_persona
#Grupo
from apps.contrato.view.views_grupo import GrupoListarView,GrupoCrearView,GrupoEditaView,GrupoDetallesView,\
    GrupoEliminarView,grupodesactivar,grupoactivar,cambiar_estado_grupo

#Cliente
from apps.contrato.view.views_cliente import ClienteListarView,ClienteCrearView,ClienteEditarView,ClienteDetalleView,\
    ClienteEliminarView,clientedesactivar,clienteactivar,cambiar_estado_cliente

#ReferenciaCelular
from apps.contrato.view.views_referenciacelular import MovilListarView,MovilCrearView,MovilEditarView,MovilDetalleView\
    ,MovilEliminarView,movildesactivar,movilactivar,cambiar_estado_movil

#Contrato
from apps.contrato.view.views_contrato import ContratoListarView,ContratoCrearView,ContratoEditarView,ContratoDetalleView,\
    ContratoEliminarView,contratodesactivar,contratoactivar,cambiar_estado_contrato,\
    manual

#Banco
from apps.contrato.view.views_banco import BancoListarView,BancoCrearView,BancoEditarView,BancoDetalleView,\
    BancoEliminarView,bancoactivar,bancodesactivar,cambiar_estado_banco

#Cuenta
from apps.contrato.view.views_cuenta import CuentaListarView,CuentaCrearView,CuentaEditarView,CuentaDetalleView,\
    CuentaEliminarView,cuentadesactivar,cuentaactivar,cambiar_estado_cuenta

#Moneda
from apps.contrato.view.views_moneda import MonedaListarView,MonedaCrearView,MonedaEditaView,MonedaDetalleView,\
    MonedaEliminarView,monedaactivar,monedadesactivar,cambiar_estado_moneda

#Urbanizacion
from apps.contrato.view.views_urbanizacion import UrbanizacionListarView

#Notaria
from apps.contrato.view.views_notaria import NotariaListarView,NotariaCrearView,NotariaEditarView,NotariaDetalleView,\
    NotariaEliminarView,notariodesactivar,notarioactivar,cambiar_estado_notario

#Propietaria
from apps.contrato.view.views_propietaria import PropietariaListarView,PropietariaCrearView,PropietariaEditarView,PropietariaDetalleView,\
    PropietariaEliminarView,propietariodesactivar,propietarioactivar,cambiar_estado_propietario

app_name = 'contrato'
#int uuid
urlpatterns = [
    #Persona
    path('listar/persona/', PersonaListarView.as_view(), name='listar_persona'),
    path('crear/persona/', PersonaCrearView.as_view(), name='crear_persona'),
    path('editar/<int:pk>/persona/', PersonaEditarView.as_view(), name='editar_persona'),
    path('detalle/<int:pk>/persona/', PersonaDetalleView.as_view(), name='detalle_persona'),
    path('eliminar/<int:pk>/persona/', PersonaEliminarView.as_view(), name='eliminar_persona'),

    path('desactivar/<int:id>/persona/', personadesactivar, name='desactivar_persona'),
    path('activar/<int:id>/persona/', personaactivar, name='activar_persona'),

    path('estado/<int:pk>/persona/', cambiar_estado_persona, name='estado_persona'),
    #

    #Grupo
    path('listar/grupo/', GrupoListarView.as_view(), name='listar_grupo'),
    path('crear/grupo/', GrupoCrearView.as_view(), name='crear_grupo'),
    path('editar/<int:pk>/grupo/', GrupoEditaView.as_view(), name='editar_grupo'),
    path('detalle/<int:pk>/grupo/', GrupoDetallesView.as_view(), name='detalle_grupo'),
    path('eliminar/<int:pk>/grupo/', GrupoEliminarView.as_view(), name='eliminar_grupo'),

    path('desactivar/<int:id>/grupo/', grupodesactivar, name='desactivar_grupo'),
    path('activar/<int:id>/grupo/', grupoactivar, name='activar_grupo'),

    path('estado/<int:pk>/grupo/', cambiar_estado_grupo, name='estado_grupo'),
    #

    ##Cliente
    path('listar/cliente/', ClienteListarView.as_view(), name='listar_cliente'),
    path('crear/cliente/', ClienteCrearView.as_view(), name='crear_cliente'),
    path('editar/<int:pk>/cliente/', ClienteEditarView.as_view(), name='editar_cliente'),
    path('eliminar/<int:pk>/cliente/', ClienteEliminarView.as_view(), name='eliminar_cliente'),
    path('detalle/<int:pk>/cliente', ClienteDetalleView.as_view(), name='detalle_cliente'),

    path('desactivar/<int:id>/cliente/', clientedesactivar, name='desactivar_cliente'),
    path('activar/<int:id>/cliente/', clienteactivar, name='activar_cliente'),

    path('estado/<int:pk>/cliente/', cambiar_estado_cliente, name='estado_cliente'),
    ##

    #ReferenciaCelular
    path('listar/movil/', MovilListarView.as_view(), name='listar_movil'),
    path('crear/movil/', MovilCrearView.as_view(), name='crear_movil'),
    path('editar/<int:pk>/movil/', MovilEditarView.as_view(), name='editar_movil'),
    path('eliminar/<int:pk>/movil/', MovilEliminarView.as_view(), name='eliminar_movil'),
    path('detalle/<int:pk>/movil', MovilDetalleView.as_view(), name='detalle_movil'),

    path('desactivar/<int:id>/movil/', movildesactivar, name='desactivar_movil'),
    path('activar/<int:id>/movil/', movilactivar, name='activar_movil'),

    path('estado/<int:pk>/movil/', cambiar_estado_movil, name='estado_movil'),
    ##

    #Contrato
    path('listar/contrato/', ContratoListarView.as_view(), name='listar_contrato'),
    path('crear/contrato/', ContratoCrearView.as_view(), name='crear_contrato'),
    path('editar/<int:pk>/contrato/', ContratoEditarView.as_view(), name='editar_contrato'),
    path('eliminar/<int:pk>/contrato/', ContratoEliminarView.as_view(), name='eliminar_contrato'),
    path('detalle/<int:pk>/contrato', ContratoDetalleView.as_view(), name='detalle_contrato'),
    #
    path('desactivar/<int:id>/contrato/', contratodesactivar, name='desactivar_contrato'),
    path('activar/<int:id>/contrato/', contratoactivar, name='activar_contrato'),
    ##rapido
    path('estado/<int:pk>/contrato/', cambiar_estado_contrato, name='estado_contrato'),
    #
    path('reporte/contrato/', manual, name='reporte_contrato'),
    #


    #
    path('reporte/contrato/', manual, name='reporte_contrato'),
    #


    # Banco
    path('listar/banco/', BancoListarView.as_view(), name='listar_banco'),
    path('crear/banco/', BancoCrearView.as_view(), name='crear_banco'),
    path('editar/<int:pk>/banco/', BancoEditarView.as_view(), name='editar_banco'),
    path('eliminar/<int:pk>/banco/', BancoEliminarView.as_view(), name='eliminar_banco'),
    path('detalle/<int:pk>/banco/', BancoDetalleView.as_view(), name='detalle_banco'),

    path('desactivar/<int:id>/banco/', bancodesactivar, name='desactivar_banco'),
    path('activar/<int:id>/banco/', bancoactivar, name='activar_banco'),

    path('estado/<int:pk>/banco/', cambiar_estado_banco, name='estado_banco'),
    #

    # Cuenta
    path('listar/cuenta/', CuentaListarView.as_view(), name='listar_cuenta'),
    path('crear/cuenta/', CuentaCrearView.as_view(), name='crear_cuenta'),
    path('editar/<int:pk>/cuenta/', CuentaEditarView.as_view(), name='editar_cuenta'),
    path('eliminar/<int:pk>/cuenta/', CuentaEliminarView.as_view(), name='eliminar_cuenta'),
    path('detalle/<int:pk>/cuenta/', CuentaDetalleView.as_view(), name='detalle_cuenta'),

    path('desactivar/<int:id>/cuenta', cuentadesactivar, name='desactivar_cuenta'),
    path('activar/<int:id>/cuenta', cuentaactivar, name='activar_cuenta'),

    path('estado/<int:pk>/cuenta/', cambiar_estado_cuenta, name='estado_cuenta'),
    #

    # Moneda
    path('listar/moneda/', MonedaListarView.as_view(), name='listar_moneda'),
    path('crear/moneda/', MonedaCrearView.as_view(), name='crear_moneda'),
    path('editar/<int:pk>/moneda/', MonedaEditaView.as_view(), name='editar_moneda'),
    path('eliminar/<int:pk>/moneda/', MonedaEliminarView.as_view(), name='eliminar_moneda'),
    path('detalle/<int:pk>/moneda/', MonedaDetalleView.as_view(), name='detalle_moneda'),

    path('desactivar/<int:id>/moneda', monedadesactivar, name='desactivar_moneda'),
    path('activar/<int:id>/moneda', monedaactivar, name='activar_moneda'),

    path('estado/<int:pk>/moneda/', cambiar_estado_moneda, name='estado_moneda'),
    #


    #Notario
    path('listar/notario/', NotariaListarView.as_view(), name='listar_notario'),
    path('crear/notario/', NotariaCrearView.as_view(), name='crear_notario'),
    path('editar/<int:pk>/notario/', NotariaEditarView.as_view(), name='editar_notario'),
    path('eliminar/<int:pk>/notario/', NotariaEliminarView.as_view(), name='eliminar_notario'),
    path('detalle/<int:pk>/notario/', NotariaDetalleView.as_view(), name='detalle_notario'),

    path('desactivar/<int:id>/notario', notariodesactivar, name='desactivar_notario'),
    path('activar/<int:id>/notario', notarioactivar, name='activar_notario'),

    path('estado/<int:pk>/notario/', cambiar_estado_notario, name='estado_notario'),
    #

    #Propietario
    path('listar/propietario/', PropietariaListarView.as_view(), name='listar_propietario'),
    path('crear/propietario/', PropietariaCrearView.as_view(), name='crear_propietario'),
    path('editar/<int:pk>/propietario/', PropietariaEditarView.as_view(), name='editar_propietario'),
    path('eliminar/<int:pk>/propietario/', PropietariaEliminarView.as_view(), name='eliminar_propietario'),
    path('detalle/<int:pk>/propietario/', PropietariaDetalleView.as_view(), name='detalle_propietario'),

    path('desactivar/<int:id>/propietario', propietariodesactivar, name='desactivar_propietario'),
    path('activar/<int:id>/propietario', propietarioactivar, name='activar_propietario'),

    path('estado/<int:pk>/propietario/', cambiar_estado_propietario, name='estado_propietario'),
    #

    #Urbanizacion
    path('urbanizacion/', UrbanizacionListarView.as_view(), name='listar_urbanizacion'),

#    path('perfil/<slug:usuario_url>/usuario/', UsuarioPerfilDetalleView.as_view(), name='perfil_usuario'),
]
