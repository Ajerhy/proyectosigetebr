from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.contrato.models import Referenciacelular
from apps.contrato.form.forms_referenciacelular import MovilForm

from django.db.models import Q

MOVIL_FIELDS = [
    {'string': 'N°'},
    {'string': 'Cliente'},
    {'string': 'Numero'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class MovilListarView(LoginRequiredMixin,generic.ListView):
class MovilListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/movil/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(MovilListarView, self).get_context_data(**kwargs)
        moviltodo = Referenciacelular.objects.all()
        movilactiva = Referenciacelular.objects.exclude(estado='True')
        context["movil_count"] = movilactiva
        context["list_movil"] = moviltodo
        context['fields'] = MOVIL_FIELDS
        return context

class MovilCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Referenciacelular
    template_name = "sigetebr/apps/contrato/movil/form.html"
    context_object_name = "obj_movil"
    form_class = MovilForm
    success_url = reverse_lazy("contrato:listar_movil")
    success_message = "Movil Creado Exitosamente"

    def form_valid(self, form):
        movil = form.save(commit=False)
        movil.uc = self.request.user.id
        movil.direccion_ip=get_ip(self.request)
        movil.save()
        return super().form_valid(form)

class MovilEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Referenciacelular
    template_name = "sigetebr/apps/contrato/movil/form.html"
    context_object_name = "obj_movil"
    form_class = MovilForm
    success_url = reverse_lazy("contrato:listar_movil")
    success_message = "Movil Actualizado Satisfactoriamente"

    def form_valid(self, form):
        movil = form.save(commit=False)
        movil.um = self.request.user.id
        movil.direccion_ip=get_ip(self.request)
        movil.save()
        return super().form_valid(form)

class MovilDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Referenciacelular
    template_name = 'sigetebr/apps/contrato/movil/detalle.html'#url
    context_object_name = 'obj'

class MovilEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Referenciacelular
    template_name= 'sigetebr/apps/contrato/movil/eliminar.html'
    context_object_name='obj_movil'
    success_url = reverse_lazy("contrato:listar_movil")
    success_message="Movil Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def movildesactivar(request, id):
    movil = Referenciacelular.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/movil/estado_desactivar.html'#url

    if not movil:
        return redirect('contrato:listar_movil')

    if request.method=='GET':
        contexto={'obj':movil}

    if request.method=='POST':
        movil.estado=False
        movil.save()
        messages.error(request, "Movil Desactivada")
        return redirect('contrato:listar_movil')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def movilactivar(request, id):
    movil = Referenciacelular.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/movil/estado_activar.html'#url

    if not movil:
        return redirect('contrato:listar_movil')

    if request.method=='GET':
        contexto={'obj':movil}

    if request.method=='POST':
        movil.estado=True
        movil.save()
        messages.success(request, "Movil Activada")
        return redirect('contrato:listar_movil')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_movil(request, pk):
    movil = get_object_or_404(Referenciacelular, pk=pk)
    if movil.estado:
        movil.estado = False
        messages.error(request, "Movil Desactivada")
    else:
        movil.estado = True
        messages.success(request, "Movil Activada")
    movil.save()
    return redirect('contrato:listar_movil')
