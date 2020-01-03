from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.contrato.models import Grupo
from apps.contrato.form.forms_grupo import GrupoForm

from django.db.models import Q

GRUPO_FIELDS = [
    {'string': 'N°'},
    {'string': 'Grupo'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class GrupoListarView(LoginRequiredMixin,generic.ListView):
class GrupoListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/grupo/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(GrupoListarView, self).get_context_data(**kwargs)
        grupotodo = Grupo.objects.all()
        grupoactiva = Grupo.objects.exclude(estado='True')
        context["grupo_count"] = grupoactiva
        context["list_grupo"] = grupotodo
        context['fields'] = GRUPO_FIELDS
        return context

#Grupo Crear
class GrupoCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Grupo
    template_name = "sigetebr/apps/contrato/grupo/form.html"
    context_object_name = "obj_grupo"
    form_class = GrupoForm
    success_url = reverse_lazy("usuario:listar_grupo")
    success_message = "Grupo Creado Exitosamente"
    login_url = 'usuario:index'

#Grupo Editar
class GrupoEditaView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Grupo
    template_name = "sigetebr/apps/contrato/grupo/form.html"
    context_object_name = "obj_grupo"
    form_class = GrupoForm
    success_url = reverse_lazy("usuario:listar_grupo")
    success_message = "Grupo Actualizada Satisfactoriamente"
    login_url = 'usuario:index'

#Grupo Detalle
class GrupoDetallesView(LoginRequiredMixin,DetailView):
    login_url = 'usuarios:index'
    model = Grupo
    template_name = 'sigetebr/apps/contrato/grupo/detalle.html'#url
    context_object_name = 'obj'

#Grupo Eliminar
class GrupoEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model = Grupo
    template_name='sigetebr/apps/contrato/grupo/eliminar.html'
    context_object_name='obj'
    success_url = reverse_lazy("usuario:listar_grupo")
    success_message="Grupo Eliminada Exitosamente"
    login_url = 'usuario:index'

#Desactivar
@login_required(login_url='usuario:index')
def grupodesactivar(request, id):
    usuario = Grupo.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/grupo/estado_desactivar.html'#url

    if not usuario:
        return redirect('usuario:listar_grupo')

    if request.method=='GET':
        contexto={'obj':usuario}

    if request.method=='POST':
        usuario.estado=False
        usuario.save()
        return redirect('usuario:listar_grupo')

    return render(request,template_name,contexto)

#Activar
@login_required(login_url='usuario:index')
def grupoactivar(request, id):
    grupo = Grupo.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/grupo/estado_activar.html'#url

    if not grupo:
        return redirect('usuario:listar_grupo')

    if request.method=='GET':
        contexto={'obj':grupo}

    if request.method=='POST':
        grupo.estado=True
        grupo.save()
        return redirect('usuario:listar_grupo')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_grupo(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    if grupo.estado:
        grupo.estado = False
        messages.error(request, "Grupo Desactivada")
    else:
        grupo.estado = True
        messages.success(request, "Grupo Activada")
    grupo.um = request.user.id
    grupo.save()
    return redirect('usuario:listar_grupo')
