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
from apps.contrato.form.forms_urbanizacion import  UrbanizacionForm
from apps.contrato.models import Urbanizacion

URBANIZACION_FIELDS = [
    {'string': 'N°'},
    {'string': 'Numero de Cuenta'},
    {'string': 'Banco'},
    {'string': 'Moneda'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class UrbanizacionListarView(LoginRequiredMixin,generic.ListView):
class UrbanizacionListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/urbanizacion/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(UrbanizacionListarView, self).get_context_data(**kwargs)
        urbanizaciontodo = Urbanizacion.objects.all()
        urbanizacionactiva = Urbanizacion.objects.exclude(estado='True')
        context["urbanizacion_count"] = urbanizacionactiva
        context["list_urbanizacion"] = urbanizaciontodo
        context['fields'] = URBANIZACION_FIELDS
        return context

class UrbanizacionCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Urbanizacion
    template_name = "sigetebr/apps/contrato/urbanizacion/form.html"
    context_object_name = "obj_urbanizacion"
    form_class = UrbanizacionForm
    success_url = reverse_lazy("contrato:listar_urbanizacion")
    success_message = "Urbanizacion Creado Exitosamente"

    def form_valid(self, form):
        urbanizacion = form.save(commit=False)
        urbanizacion.uc = self.request.user.id
        urbanizacion.direccion_ip=get_ip(self.request)
        urbanizacion.save()
        return super().form_valid(form)

#Urbanizacion DetalleView
class UrbanizacionDetalleView(LoginRequiredMixin,DetailView):
    model = Urbanizacion
    template_name = 'sigetebr/apps/contrato/urbanizacion/listar.html'  # url
    slug_field = 'usuario'#que campo de la base de datos
    slug_url_kwarg = 'usuario_url'#que campo de la url
    login_url = 'usuario:index'