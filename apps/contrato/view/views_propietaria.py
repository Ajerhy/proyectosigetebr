from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from apps.usuario.templatetags.utils import get_ip
from django.db.models import Q

from apps.contrato.form.forms_propietaria import PropietariaForm
from apps.contrato.models import Propietaria

PROPIETARIA_FIELDS = [
    {'string': 'N°'},
    {'string': 'Persona'},
    {'string': 'Actividad'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class PropietariaListarView(LoginRequiredMixin,generic.ListView):
class PropietariaListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/propietario/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(PropietariaListarView, self).get_context_data(**kwargs)
        propietariotodo = Propietaria.objects.all()
        propietarioactiva = Propietaria.objects.exclude(estado='True')
        context["propietario_count"] = propietarioactiva
        context["list_propietario"] = propietariotodo
        context['fields'] = PROPIETARIA_FIELDS
        return context

class PropietariaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Propietaria
    template_name = "sigetebr/apps/contrato/propietario/form.html"
    context_object_name = "obj_propietario"
    form_class = PropietariaForm
    success_url = reverse_lazy("contrato:listar_propietario")
    success_message = "Propietaria Creado Exitosamente"

    def form_valid(self, form):
        propietario = form.save(commit=False)
        propietario.uc = self.request.user.id
        propietario.direccion_ip=get_ip(self.request)
        propietario.save()
        return super().form_valid(form)

class PropietariaEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Propietaria
    template_name = "sigetebr/apps/contrato/propietario/form.html"
    context_object_name = "obj_propietario"
    form_class = Propietaria
    success_url = reverse_lazy("contrato:listar_propietario")
    success_message = "Propietaria Actualizado Satisfactoriamente"

    def form_valid(self, form):
        propietario = form.save(commit=False)
        propietario.um = self.request.user.id
        propietario.direccion_ip=get_ip(self.request)
        propietario.save()
        return super().form_valid(form)

class PropietariaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Propietaria
    template_name = 'sigetebr/apps/contrato/propietario/detalle.html'#url
    context_object_name = 'obj'

class PropietariaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Propietaria
    template_name= 'sigetebr/apps/contrato/propietario/eliminar.html'
    context_object_name='obj_propietario'
    success_url = reverse_lazy("contrato:listar_propietario")
    success_message="Propietaria Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def propietariodesactivar(request, id):
    propietario = Propietaria.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/propietario/estado_desactivar.html'#url

    if not propietario:
        return redirect('contrato:listar_propietario')

    if request.method=='GET':
        contexto={'obj':propietario}

    if request.method=='POST':
        propietario.estado=False
        propietario.save()
        messages.error(request, "Propietaria Desactivada")
        return redirect('contrato:listar_propietario')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def propietarioactivar(request, id):
    propietario = Propietaria.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/propietario/estado_activar.html'#url

    if not propietario:
        return redirect('contrato:listar_propietario')

    if request.method=='GET':
        contexto={'obj':propietario}

    if request.method=='POST':
        propietario.estado=True
        propietario.save()
        messages.success(request, "Propietaria Activada")
        return redirect('contrato:listar_propietario')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_propietario(request, pk):
    propietario = get_object_or_404(Propietaria, pk=pk)
    if propietario.estado:
        propietario.estado = False
        messages.error(request, "Propietaria Desactivada")
    else:
        propietario.estado = True
        messages.success(request, "Propietaria Activada")
    propietario.save()
    return redirect('contrato:listar_propietario')
