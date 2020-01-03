from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from apps.usuario.templatetags.utils import get_ip
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
import json

from apps.usuario.form.forms_perfil import LoginUsuarioPerfilForm,\
    PasswordUsuarioPerfilForm,EditarUsuarioPerfilForm,\
    PerfilFrom

from django.db.models import Q

from apps.usuario.models import Perfil
from apps.contrato.models import Persona
from apps.contrato.models import Cliente
from apps.terreno.models import Manzano,Lote

#Login
class LoginPerfilView(TemplateView,LoginRequiredMixin):
    login_url = 'usuario:index'
    template_name = "sigetebr/apps/usuario/index.html"#url
    success_url = reverse_lazy("usuario:dashboard")#ur

    def get_context_data(self, **kwargs):
        context = super(LoginPerfilView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(LoginPerfilView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginUsuarioPerfilForm(request.POST, request=request)
        if form.is_valid():
            #user = Perfil.objects.filter(usuario=request.POST.get('usuario')).first()
            perfil = Perfil.objects.filter(usuario=request.POST.get('usuario')).first()

            if perfil is not None:
                if perfil.estado:
                    perfil = authenticate(
                        usuario=request.POST.get('usuario'),
                        password=request.POST.get('password'))
                    if perfil is not None:
                        login_django(request, perfil)
                        return redirect('usuario:dashboard')
                        #return HttpResponseRedirect('usuarios:dashboard')
                    return render(request,  self.template_name, {
                        "error": True,
                        "message": "Tu nombre de usuario y contraseña no coinciden. Inténtalo de nuevo."}
                                  )
                return render(request,  self.template_name, {
                    "error": True,
                    "message": "Su cuenta está inactiva. Por favor, póngase en contacto con el administrador"}
                              )
            return render(request,  self.template_name, {
                "error": True,
                "message": "Tu cuenta no se encuentra. Por favor, póngase en contacto con el administrador"}
                          )
        return render(request,  self.template_name, {
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


        usuariotodo = Perfil.objects.all()
        usuariodmin = Perfil.objects.exclude(is_superuser='True')
        usuarioactiva = Perfil.objects.exclude(is_active='True')
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
    model = Perfil
    template_name = 'sigetebr/apps/usuario/configuracion/perfil_usuario.html'  # url
    slug_field = 'usuario'#que campo de la base de datos
    slug_url_kwarg = 'usuario_url'#que campo de la url
    login_url = 'usuarios:index'

#Usuario Perfil Actualizar Usuario
class UsuarioPerfilEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Perfil
    form_class = EditarUsuarioPerfilForm
    template_name = 'sigetebr/apps/usuario/configuracion/perfil_form.html'  # url
    success_url = reverse_lazy('usuarios:perfil_actualizar')
#    success_message = "Tu usuario ha sido actualizado"
    context_object_name = "user_obj"
    login_url = 'usuarios:index'

    def form_valid(self, form):
        messages.success(self.request, "Tu Perfil Usuario ha sido actualizado")
        return super(UsuarioPerfilEditarView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

#Usuario Perfil Actualizar Password Usuario
@login_required(login_url='usuarios:index')
def passwordusuarioview(request):
    template_name = 'sigetebr/apps/usuario/configuracion/perfil_password.html'  # url
    form = PasswordUsuarioPerfilForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            actual = request.POST.get('password')
            nuevo = request.POST.get('password')
            confirma =request.POST.get('confimar_password')
            print(actual)
            print(nuevo)
            print(confirma)
            if not check_password(request.POST.get('password'), request.user.password):
                messages.warning(request, 'Password Actual no coinciden!')
            else:
                if authenticate(usuario = request.user.usuario,password = request.POST.get('password')):
                    request.user.set_password(request.POST.get('new_password'))
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Password Actualizado!')
                    #redirect()
        else:
            messages.error(request, 'Verifique su Password por favor!')
    context = {'form': form}
    return render(request, template_name, context)

USUARIO_FIELDS = [
    {'string': 'N°', 'field': 'numero'},
    {'string': 'Usuario', 'field': 'usuario'},
    {'string': 'Nombres', 'field': 'nombre'},
    {'string': 'Email', 'field': 'email'},
    {'string': 'Roles', 'field': 'roles'},
    {'string': 'Estado', 'field': 'estado'},
    {'string': 'Acciones', 'field': 'acciones'},
]

#class PerfilListarView(LoginRequiredMixin,generic.ListView):
class PerfilListarView(LoginRequiredMixin,TemplateView):
    model = Perfil
    template_name = "sigetebr/apps/usuario/perfil/listar.html"
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
        context = super(PerfilListarView, self).get_context_data(**kwargs)
        context["list_perfil"] = self.get_queryset()
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

#Perfil Crear
class PerfilCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Perfil
    template_name = "sigetebr/apps/usuario/perfil/form.html"
    context_object_name = "obj"
    form_class = PerfilFrom
    success_url = reverse_lazy("usuario:listar_perfil")
    success_message = "Perfil de Usuario Creado Exitosamente"
    login_url = 'usuario:index'

#Perfil Editar
class PerfilEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Perfil
    template_name = "sigetebr/apps/usuario/perfil/form.html"
    context_object_name = "obj_usuario"
    form_class = PerfilFrom
    success_url = reverse_lazy("usuario:listar_perfil")
    success_message = "Perfil de Usuario Actualizada Satisfactoriamente"
    login_url = 'usuario:index'

#Perfil Detalle
class PerfilDetallesView(LoginRequiredMixin,DetailView):
    model = Perfil
    template_name = 'sigetebr/apps/usuario/perfil/detalle.html'#url
    slug_field = 'usuario'#que campo de la base de datos
    context_object_name = 'obj'
    slug_url_kwarg = 'usuario_url'#que campo de la url
    login_url = 'usuario:index'

#Perfil Eliminar
class PerfilEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model = Perfil
    template_name='sigetebr/apps/usuario/perfil/eliminar.html'
    context_object_name='obj'
    success_url = reverse_lazy("usuario:listar_perfil")
    success_message="Perfil de Usuario Eliminada Exitosamente"
    login_url = 'usuario:index'

#Desactivar
@login_required(login_url='usuario:index')
def perfildesactivar(request, id):
    perfil = Perfil.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/usuario/perfil/estado_desactivar.html'#url

    if not perfil:
        return redirect('usuario:listar_perfil')

    if request.method=='GET':
        contexto={'obj':perfil}

    if request.method=='POST':
        perfil.estado=False
        perfil.save()
        return redirect('usuario:listar_perfil')

    return render(request,template_name,contexto)

#Activar
@login_required(login_url='usuario:index')
def perfilactivar(request, id):
    perfil = Perfil.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/usuario/perfil/estado_activar.html'#url

    if not perfil:
        return redirect('usuario:listar_perfil')

    if request.method=='GET':
        contexto={'obj':perfil}

    if request.method=='POST':
        perfil.estado=True
        perfil.save()
        return redirect('usuario:listar_perfil')

    return render(request,template_name,contexto)

#Estado
@login_required(login_url='usuario:index')
def cambiar_estado_perfil(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if perfil.estado:
        perfil.estado = False
        messages.error(request, "Perfil de Usuario Desactivada")
    else:
        perfil.estado = True
        messages.success(request, "Perfil de Usuario Activada")
    perfil.um = request.user.id
    perfil.save()
    return redirect('usuario:listar_perfil')
