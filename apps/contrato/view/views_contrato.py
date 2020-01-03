from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.contrato.models import Contrato
from apps.contrato.form.forms_contrato import ContratoForm

from django.db.models import Q

@login_required(login_url='usuario:index')
def manual(request):
    return render(request, template_name='sigetebr/apps/contrato/contrato/reporte.html')

CONTRATO_FIELDS = [
    {'string': 'N°'},
    {'string': 'Cliente'},
    {'string': 'Lotes - Manzano'},
    {'string': 'Tipo Pago'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class ContratoListarView(LoginRequiredMixin,generic.ListView):
class ContratoListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/contrato/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(ContratoListarView, self).get_context_data(**kwargs)
        contratotodo = Contrato.objects.all()
        contratoactiva = Contrato.objects.exclude(estado='True')
        context["contrato_count"] = contratoactiva
        context["list_contrato"] = contratotodo
        context['fields'] = CONTRATO_FIELDS
        return context

class ContratoCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Contrato
    template_name = "sigetebr/apps/contrato/contrato/form.html"
    context_object_name = "obj_contrato"
    form_class = ContratoForm
    success_url = reverse_lazy("contrato:listar_contrato")
    success_message = "Contrato Creada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        contrato = form.save(commit=False)
        contrato.uc = self.request.user
        contrato.direccion_ip=get_ip(self.request)
        contrato.save()
        return super().form_valid(form)

class ContratoEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Contrato
    template_name = "sigetebr/apps/contrato/contrato/form.html"
    form_class = ContratoForm
    context_object_name = "obj_contrato"
    success_url = reverse_lazy("contrato:listar_contrato")
    success_message = "Contrato Modificada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        contrato = form.save(commit=False)
        contrato.um = self.request.user.id
        contrato.direccion_ip=get_ip(self.request)
        contrato.save()
        return super().form_valid(form)

class ContratoDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Contrato
    template_name = 'sigetebr/apps/contrato/contrato/detalle.html'#url
    context_object_name = 'obj'

class ContratoEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Contrato
    template_name= 'sigetebr/apps/contrato/contrato/eliminar.html'
    context_object_name='obj_medida'
    success_url = reverse_lazy("contrato:listar_contrato")
    success_message="Contrato Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def contratodesactivar(request, id):
    contrato = Contrato.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/contrato/estado_desactivar.html'#url

    if not contrato:
        return redirect('contrato:listar_contrato')

    if request.method=='GET':
        contexto={'obj':contrato}

    if request.method=='POST':
        contrato.estado=False
        contrato.save()
        messages.error(request, "Contrato Desactivada")
        return redirect('contrato:listar_contrato')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def contratoactivar(request, id):
    contrato = Contrato.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/contrato/estado_activar.html'#url

    if not contrato:
        return redirect('contrato:listar_contrato')

    if request.method=='GET':
        contexto={'obj':contrato}

    if request.method=='POST':
        contrato.estado=True
        contrato.save()
        messages.success(request, "Contrato Activada")
        return redirect('contrato:listar_contrato')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if contrato.estado:
        contrato.estado = False
        messages.error(request, "Contrato Desactivada")
    else:
        contrato.estado = True
        messages.success(request, "Contrato Activada")
    contrato.um = request.user.id
    contrato.direccion_ip = get_ip(request)
    contrato.save()
    return redirect('contrato:listar_contrato')
