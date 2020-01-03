from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.terreno.models import Distrito
from apps.contrato.form.forms_grupo import GrupoForm

from django.db.models import Q

DISTRITO_FIELDS = [
    {'string': 'N°'},
    {'string': 'Numero'},
    {'string': 'Nombre'},
    {'string': 'Sigla'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class DistritoListarView(LoginRequiredMixin,generic.ListView):
class DistritoListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/terreno/distrito/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(DistritoListarView, self).get_context_data(**kwargs)
        distritotodo = Distrito.objects.all()
        distritoactiva = Distrito.objects.exclude(estado='True')
        context["distrito_count"] = distritoactiva
        context["list_distrito"] = distritotodo
        context['fields'] = DISTRITO_FIELDS
        return context