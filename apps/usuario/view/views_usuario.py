from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import json
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from apps.usuario.models import Usuario
from apps.contrato.models import Persona
from apps.contrato.models import Cliente
from apps.terreno.models import Manzano,Lote


from apps.usuario.form.forms_usuario import LoginUsuarioForm,\
    ActualizarUsuarioForm,ActualizarPasswordForm,\
    UsuarioForm

#Login
class LoginView(TemplateView,LoginRequiredMixin):
    login_url = 'usuario:index'
    template_name = "sigetebr/apps/usuario/index.html"#url
    success_url = reverse_lazy("usuario:dashboard")#url

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginUsuarioForm(request.POST, request=request)
        if form.is_valid():
            user = Usuario.objects.filter(usuario=request.POST.get('usuario')).first()
            if user is not None:
                if user.is_active:
                    user = authenticate(
                        usuario=request.POST.get('usuario'),
                        password=request.POST.get('password'))
                    if user is not None:
                        login_django(request, user)
                        return redirect('usuario:dashboard')
                    return render(request, self.template_name, {
                        "error": True,
                        "message": "Tu nombre de usuario y contraseña no coinciden. Inténtalo de nuevo."}
                                  )
                return render(request, self.template_name, {
                    "error": True,
                    "message": "Su cuenta está inactiva. Por favor, póngase en contacto con el administrador"}
                              )
            return render(request, self.template_name, {
                "error": True,
                "message": "Tu cuenta no se encuentra. Por favor, póngase en contacto con el administrador"}
                          )
        return render(request, self.template_name, {
            # "error": True,
            # "message": "Tu nombre de Usuario y Contraseña no coinciden. Inténtalo de nuevo."
            "form": form
        })

#Dashboard
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/dashboard.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        manzanostodo = Manzano.objects.all()
        manzanosactiva = Manzano.objects.exclude(estado='False')
        context["manzanos"] = manzanostodo
        context["manzano_count"] = manzanosactiva

        lotestodo = Lote.objects.all()
        lotesactiva = Lote.objects.exclude(estado='False')
        context["lotes"] = lotestodo
        context["lote_count"] = lotesactiva


        usuariotodo = Usuario.objects.all()
        usuariodmin = Usuario.objects.exclude(is_superuser='True')
        usuarioactiva = Usuario.objects.exclude(is_active='True')
        context["usuario_count"] = usuarioactiva
        context["usuarios"] = usuariotodo

        personatodo = Persona.objects.all()
        personaactiva = Persona.objects.exclude(estado='False')
        context["persona_count"] = personaactiva
        context["personas"] = personatodo

        clientetodo = Cliente.objects.all()
        clienteactiva = Cliente.objects.exclude(estado='False')
        context["cliente_count"] = clienteactiva
        context["clientes"] = clientetodo

        return context

"""
Funciones
"""
#Salir
@login_required(login_url='usuario:index')
def LogoutView(request):
    logout_django(request)
    return redirect('usuario:index')


#Usuario Perfil Usuario
class UsuarioPerfilDetalleView(LoginRequiredMixin,DetailView):
    model = Usuario
    template_name = 'sigetebr/apps/usuario/perfil/listar.html'  # url
    slug_field = 'usuario'#que campo de la base de datos
    slug_url_kwarg = 'usuario_url'#que campo de la url
    login_url = 'usuarios:index'



USUARIO_FIELDS = [
    {'string': 'N°', 'field': 'numero'},
    {'string': 'Usuario', 'field': 'usuario'},
    {'string': 'Nombres', 'field': 'nombre'},
    {'string': 'Email', 'field': 'email'},
    {'string': 'Estado', 'field': 'estado'},
    {'string': 'Acciones', 'field': 'acciones'},
]

#class UsuarioListarView(LoginRequiredMixin,generic.ListView):
class UsuarioListarView(LoginRequiredMixin,TemplateView):
    model = Usuario
    template_name = "sigetebr/apps/usuario/usuario/listar.html"
    #context_object_name = "list_usuario"
    login_url = 'usuario:index'

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        print(request_post,"Usuario")
        if request_post:
            if request_post.get('usuario'):
                queryset = queryset.filter(
                    usuario__icontains=request_post.get('usuario'))
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email'))
        print(queryset, "Resultado")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsuarioListarView, self).get_context_data(**kwargs)
        context["list_usuario"] = self.get_queryset()
        context['fields'] = USUARIO_FIELDS
        context["per_page"] = self.request.POST.get('per_page')

        search = False
        if (
                self.request.POST.get('usuario') or
                self.request.POST.get('email')
        ):
            search = True
        context["search"] = search

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

#Usuario Crear
class UsuarioCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Usuario
    template_name = "sigetebr/apps/usuario/usuario/form.html"
    context_object_name = "obj"
    form_class = UsuarioForm
    success_url = reverse_lazy("usuario:listar_usuario")
    success_message = "Usuario Creado Exitosamente"
    login_url = 'usuario:index'

#Usuario Editar
class UsuarioEditaView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Usuario
    template_name = "sigetebr/apps/usuario/usuario/form.html"
    context_object_name = "obj_usuario"
    form_class = UsuarioForm
    success_url = reverse_lazy("usuario:listar_usuario")
    success_message = "Usuario Actualizada Satisfactoriamente"
    login_url = 'usuario:index'

#Usuario Detalle
class UsuarioDetallesView(LoginRequiredMixin,DetailView):
    model = Usuario
    template_name = 'sigetebr/apps/usuario/usuario/detalle.html'#url
    slug_field = 'usuario'#que campo de la base de datos
    context_object_name = 'obj'
    slug_url_kwarg = 'usuario_url'#que campo de la url
    login_url = 'usuario:index'

#Usuario Eliminar
class UsuarioEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name='sigetebr/apps/usuario/usuario/eliminar.html'
    context_object_name='obj'
    success_url = reverse_lazy("usuario:listar_usuario")
    success_message="Usuario Eliminada Exitosamente"
    login_url = 'usuario:index'

#Desactivar
@login_required(login_url='usuario:index')
def usuariodesactivar(request, id):
    usuario = Usuario.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/usuario/usuario/estado_desactivar.html'#url

    if not usuario:
        return redirect('usuario:listar_usuario')

    if request.method=='GET':
        contexto={'obj':usuario}

    if request.method=='POST':
        usuario.is_active=False
        usuario.save()
        return redirect('usuario:listar_usuario')

    return render(request,template_name,contexto)

#Activar
@login_required(login_url='usuario:index')
def usuarioactivar(request, id):
    usuario = Usuario.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/usuario/usuario/estado_activar.html'#url

    if not usuario:
        return redirect('usuario:listar_usuario')

    if request.method=='GET':
        contexto={'obj':usuario}

    if request.method=='POST':
        usuario.is_active=True
        usuario.save()
        return redirect('usuario:listar_usuario')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario.is_active:
        usuario.is_active = False
        messages.error(request, "Usuario Desactivada")
    else:
        usuario.is_active = True
        messages.success(request, "Usuario Activada")
    usuario.um = request.user.id
    usuario.save()
    return redirect('usuario:listar_usuario')




"""
        personatodo = Persona.objects.all()
        personaactiva = Persona.objects.exclude(estado='False')
        context["persona_count"] = personaactiva
        context["personas"] = personatodo
        instituciontodo = Institucion.objects.all()
        institucionactiva = Institucion.objects.exclude(estado='False')

        serviciotodo = Servicio.objects.all()
        servicioactiva = Servicio.objects.exclude(estado='False')

        context["persona_count"] = personaactiva
        context["personas"] = personatodo

        context["institucion_count"] = institucionactiva
        context["instituciones"] = instituciontodo

        context["servicio_count"] = servicioactiva
        context["servicios"] = serviciotodo

        pp = ((100*personaactiva.count())/personatodo.count())
        context["pp"] = round(pp)
        pi = ((100*institucionactiva.count())/instituciontodo.count())
        context["pi"] = round(pi)


        print(pp,"ppppppppppppppppppppppppppppppppppp")
        print(pi, "pipipipipipipipipipipipipipipipipi")
"""