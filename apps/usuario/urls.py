from django.urls import path

#Perfil Usuario Login
from apps.usuario.view.views_perfil import LoginPerfilView,DashboardView,LogoutView,UsuarioPerfilDetalleView,UsuarioPerfilEditarView,passwordusuarioview

#Usuario
from apps.usuario.view.views_usuario import UsuarioListarView,UsuarioCrearView,UsuarioEditaView,UsuarioDetallesView,\
    UsuarioEliminarView,usuariodesactivar,usuarioactivar,cambiar_estado_usuario

#Perfil
from apps.usuario.view.views_perfil import PerfilListarView

app_name = 'usuario'
#int uuid
urlpatterns = [
    # Login
    path('', LoginPerfilView.as_view(), name='index'),
    path('logout/', LogoutView, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    #Configuracion
    path('perfil/<slug:usuario_url>/usuario/', UsuarioPerfilDetalleView.as_view(), name='perfil_usuario'),
    path('perfil/usuario', UsuarioPerfilEditarView.as_view(), name='perfil_actualizar'),
    path('perfil/password/', passwordusuarioview, name='cambiar_password'),

    #Usuario
    path('listar/usuario/', UsuarioListarView.as_view(), name='listar_usuario'),
    path('crear/usuario/', UsuarioCrearView.as_view(), name='crear_usuario'),
    path('editar/<int:pk>/usuario/', UsuarioEditaView.as_view(), name='editar_usuario'),
    path('detalle/<int:pk>/usuario/', UsuarioDetallesView.as_view(), name='detalle_usuario'),
    path('eliminar/<int:pk>/usuario/', UsuarioEliminarView.as_view(), name='eliminar_usuario'),
    #
    path('desactivar/<int:id>/usuario/', usuariodesactivar, name='desactivar_usuario'),
    path('activar/<int:id>/usuario/', usuarioactivar, name='activar_usuario'),
    ##rapido
    path('estado/<int:pk>/usuario/', cambiar_estado_usuario, name='estado_usuario'),
    #

    # Perfil
    path('listar/perfil/', PerfilListarView.as_view(), name='listar_perfil'),
    path('crear/perfil/', UsuarioCrearView.as_view(), name='crear_perfil'),
    path('editar/<int:pk>/perfil/', UsuarioEditaView.as_view(), name='editar_perfil'),
    path('detalle/<int:pk>/perfil/', UsuarioDetallesView.as_view(), name='detalle_perfil'),
    path('eliminar/<int:pk>/perfil/', UsuarioEliminarView.as_view(), name='eliminar_perfil'),
    #
    path('desactivar/<int:id>/perfil/', usuariodesactivar, name='desactivar_perfil'),
    path('activar/<int:id>/perfil/', usuarioactivar, name='activar_perfil'),
    ##rapido
    path('estado/<int:pk>/perfil/', cambiar_estado_usuario, name='estado_perfil'),
    #


]
