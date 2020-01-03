from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.contrato.models import Cliente
from apps.contrato.form.forms_grupo import GrupoForm
from apps.contrato.form.forms_cliente import ClienteForm
from django.db.models import Q

CLIENTE_FIELDS = [
    {'string': 'N°'},
    {'string': 'Persona'},
    {'string': 'Ci'},
    {'string': 'Grupo'},
    {'string': 'Email'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class ClienteListarView(LoginRequiredMixin,generic.ListView):
class ClienteListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/cliente/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(ClienteListarView, self).get_context_data(**kwargs)
        clientetodo = Cliente.objects.all()
        clienteactiva = Cliente.objects.exclude(estado='True')
        context["cliente_count"] = clienteactiva
        context["list_cliente"] = clientetodo
        context['fields'] = CLIENTE_FIELDS
        return context

class ClienteCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Cliente
    template_name = "sigetebr/apps/contrato/cliente/form.html"
    context_object_name = "obj_cliente"
    form_class = ClienteForm
    success_url = reverse_lazy("contrato:listar_cliente")
    success_message = "Cliente Creado Exitosamente"

    def form_valid(self, form):
        cliente = form.save(commit=False)
        cliente.uc = self.request.user.id
        cliente.direccion_ip=get_ip(self.request)
        cliente.save()
        return super().form_valid(form)

class ClienteEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Cliente
    template_name = "sigetebr/apps/contrato/cliente/form.html"
    context_object_name = "obj_Cliente"
    form_class = ClienteForm
    success_url = reverse_lazy("contrato:listar_cliente")
    success_message = "Cliente Actualizado Satisfactoriamente"

    def form_valid(self, form):
        cliente = form.save(commit=False)
        cliente.um = self.request.user.id
        cliente.direccion_ip=get_ip(self.request)
        cliente.save()
        return super().form_valid(form)

class ClienteDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Cliente
    template_name = 'sigetebr/apps/contrato/cliente/detalle.html'#url
    context_object_name = 'obj'

class ClienteEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Cliente
    template_name= 'sigetebr/apps/contrato/cliente/eliminar.html'
    context_object_name='obj_cliente'
    success_url = reverse_lazy("contrato:listar_cliente")
    success_message="Cliente Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def clientedesactivar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/cliente/estado_desactivar.html'#url

    if not cliente:
        return redirect('contrato:listar_cliente')

    if request.method=='GET':
        contexto={'obj':cliente}

    if request.method=='POST':
        cliente.estado=False
        cliente.save()
        messages.error(request, "Cliente Desactivada")
        return redirect('contrato:listar_cliente')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def clienteactivar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/cliente/estado_activar.html'#url

    if not cliente:
        return redirect('contrato:listar_cliente')

    if request.method=='GET':
        contexto={'obj':cliente}

    if request.method=='POST':
        cliente.estado=True
        cliente.save()
        messages.success(request, "Cliente Activada")
        return redirect('contrato:listar_cliente')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.estado:
        cliente.estado = False
        messages.error(request, "Cliente Desactivada")
    else:
        cliente.estado = True
        messages.success(request, "Cliente Activada")
    cliente.save()
    return redirect('contrato:listar_cliente')
