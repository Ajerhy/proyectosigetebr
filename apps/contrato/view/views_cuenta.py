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

from apps.contrato.form.forms_cuenta import CuentaForm
from apps.contrato.models import Cuenta

CUENTA_FIELDS = [
    {'string': 'N°'},
    {'string': 'Cuenta'},
    {'string': 'Banco'},
    {'string': 'Moneda'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class CuentaListarView(LoginRequiredMixin,generic.ListView):
class CuentaListarView(LoginRequiredMixin, TemplateView):
    model = Cuenta
    template_name = "sigetebr/apps/contrato/cuenta/listar.html"
    #context_object_name = "list_cuenta"
    login_url = 'usuario:index'

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        print(request_post, "Cuenta")
        if request_post:
            if request_post.get('cuenta'):
                queryset = queryset.filter(numerocuenta__icontains=request_post.get('cuenta'))
            if request_post.get('banco'):
                queryset = queryset.filter(
                    Q(banco__nombrebanco__icontains=request_post.get('banco')) &
                    Q(banco__siglabanco__icontains=request_post.get('banco'))
                )
            if request_post.get('moneda'):
                queryset = queryset.filter(
                    Q(moneda__nombremoneda__icontains=request_post.get('moneda')) &
                    Q(moneda__siglamoneda__icontains=request_post.get('moneda'))
                )
        print(queryset, "Resultado")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CuentaListarView, self).get_context_data(**kwargs)
        context["list_cuenta"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context['fields'] = CUENTA_FIELDS

        search = False
        if (
                self.request.POST.get('cuenta') or
                self.request.POST.get('banco') or
                self.request.POST.get('moneda')
        ):
            search = True
        context["search"] = search

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class CuentaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Cuenta
    template_name = "sigetebr/apps/contrato/cuenta/form.html"
    context_object_name = "obj_cuenta"
    form_class = CuentaForm
    success_url = reverse_lazy("cooperativa:listar_cuenta")
    success_message = "Cuenta Creado Exitosamente"

    def form_valid(self, form):
        cuenta = form.save(commit=False)
        cuenta.uc = self.request.user.id
        cuenta.direccion_ip=get_ip(self.request)
        cuenta.save()
        return super().form_valid(form)

class CuentaEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Cuenta
    template_name = "sigetebr/apps/contrato/cuenta/form.html"
    context_object_name = "obj_cuenta"
    form_class = CuentaForm
    success_url = reverse_lazy("cooperativa:listar_cuenta")
    success_message = "Cuenta Actualizada Satisfactoriamente"

    def form_valid(self, form):
        cuenta = form.save(commit=False)
        cuenta.um = self.request.user.id
        cuenta.direccion_ip=get_ip(self.request)
        cuenta.save()
        return super().form_valid(form)

class CuentaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Cuenta
    template_name = 'sigetebr/apps/contrato/cuenta/detalle.html'#url
    context_object_name = 'obj'

class CuentaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Cuenta
    template_name= 'sigetebr/apps/contrato/cuenta/eliminar.html'
    context_object_name='obj_cuenta'
    success_url = reverse_lazy("cooperativa:listar_cuenta")
    success_message="Cuenta Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def cuentadesactivar(request, id):
    cuenta = Cuenta.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/cuenta/estado_desactivar.html'#url

    if not cuenta:
        return redirect('cooperativa:listar_cuenta')

    if request.method=='GET':
        contexto={'obj':cuenta}

    if request.method=='POST':
        cuenta.estado=False
        cuenta.um = request.user.id
        cuenta.save()
        messages.error(request, "Banco Desactivada")
        return redirect('cooperativa:listar_cuenta')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cuentaactivar(request, id):
    cuenta = Cuenta.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/cuenta/estado_activar.html'#url

    if not cuenta:
        return redirect('cooperativa:listar_cuenta')

    if request.method=='GET':
        contexto={'obj':cuenta}

    if request.method=='POST':
        cuenta.estado=True
        cuenta.um = request.user.id
        cuenta.save()
        messages.success(request, "Banco Activada")
        return redirect('cooperativa:listar_cuenta')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_cuenta(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)
    if cuenta.estado:
        cuenta.estado = False
        messages.error(request, "Cuenta Desactivada")
    else:
        cuenta.estado = True
        messages.success(request, "Cuenta Activada")
    cuenta.um = request.user.id
    cuenta.save()
    return redirect('cooperativa:listar_cuenta')
