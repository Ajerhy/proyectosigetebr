from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.terreno.models import Ubicacion
from apps.contrato.form.forms_grupo import GrupoForm

from django.db.models import Q

UBICACION_FIELDS = [
    {'string': 'N°'},
    {'string': 'Latitud'},
    {'string': 'Longitud'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class UbicacionListarView(LoginRequiredMixin,generic.ListView):
class UbicacionListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/terreno/ubicacion/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(UbicacionListarView, self).get_context_data(**kwargs)
        ubicaciontodo = Ubicacion.objects.all()
        ubicacionactiva = Ubicacion.objects.exclude(estado='True')
        context["ubicacion_count"] = ubicacionactiva
        context["list_ubicacion"] = ubicaciontodo
        context['fields'] = UBICACION_FIELDS
        return context