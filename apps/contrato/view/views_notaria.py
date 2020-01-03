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

from apps.contrato.form.forms_notaria import NotariaForm
from apps.contrato.models import Notaria

NOTARIA_FIELDS = [
    {'string': 'N°'},
    {'string': 'Numero Notaria'},
    {'string': 'Persona'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class NotariaListarView(LoginRequiredMixin,generic.ListView):
class NotariaListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/notario/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(NotariaListarView, self).get_context_data(**kwargs)
        notariotodo = Notaria.objects.all()
        notarioactiva = Notaria.objects.exclude(estado='True')
        context["notario_count"] = notarioactiva
        context["list_notario"] = notariotodo
        context['fields'] = NOTARIA_FIELDS
        return context

class NotariaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Notaria
    template_name = "sigetebr/apps/contrato/notario/form.html"
    context_object_name = "obj_notario"
    form_class = NotariaForm
    success_url = reverse_lazy("contrato:listar_notario")
    success_message = "Notaria Creado Exitosamente"

    def form_valid(self, form):
        notario = form.save(commit=False)
        notario.uc = self.request.user.id
        notario.direccion_ip=get_ip(self.request)
        notario.save()
        return super().form_valid(form)

class NotariaEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Notaria
    template_name = "sigetebr/apps/contrato/notario/form.html"
    context_object_name = "obj_notario"
    form_class = NotariaForm
    success_url = reverse_lazy("contrato:listar_notario")
    success_message = "Notaria Actualizado Satisfactoriamente"

    def form_valid(self, form):
        notario = form.save(commit=False)
        notario.um = self.request.user.id
        notario.direccion_ip=get_ip(self.request)
        notario.save()
        return super().form_valid(form)

class NotariaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Notaria
    template_name = 'sigetebr/apps/contrato/notario/detalle.html'#url
    context_object_name = 'obj'

class NotariaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Notaria
    template_name= 'sigetebr/apps/contrato/notario/eliminar.html'
    context_object_name='obj_notario'
    success_url = reverse_lazy("contrato:listar_notario")
    success_message="Notaria Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def notariodesactivar(request, id):
    notario = Notaria.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/notario/estado_desactivar.html'#url

    if not notario:
        return redirect('contrato:listar_notario')

    if request.method=='GET':
        contexto={'obj':notario}

    if request.method=='POST':
        notario.estado=False
        notario.save()
        messages.error(request, "Notaria Desactivada")
        return redirect('contrato:listar_notario')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def notarioactivar(request, id):
    notario = Notaria.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/notario/estado_activar.html'#url

    if not notario:
        return redirect('contrato:listar_notario')

    if request.method=='GET':
        contexto={'obj':notario}

    if request.method=='POST':
        notario.estado=True
        notario.save()
        messages.success(request, "Notaria Activada")
        return redirect('contrato:listar_notario')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_notario(request, pk):
    notario = get_object_or_404(Notaria, pk=pk)
    if notario.estado:
        notario.estado = False
        messages.error(request, "Notaria Desactivada")
    else:
        notario.estado = True
        messages.success(request, "Notaria Activada")
    notario.save()
    return redirect('contrato:listar_notario')
