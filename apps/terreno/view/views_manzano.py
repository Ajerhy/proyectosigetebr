from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.terreno.models import Manzano
from apps.contrato.form.forms_grupo import GrupoForm

from django.db.models import Q

MANZANO_FIELDS = [
    {'string': 'N°'},
    {'string': 'Codigo'},
    {'string': 'Numero'},
    {'string': 'Sigla'},
    {'string': 'Lotes'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class ManzanoListarView(LoginRequiredMixin,generic.ListView):
class ManzanoListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/terreno/manzano/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(ManzanoListarView, self).get_context_data(**kwargs)
        manzanotodo = Manzano.objects.all()
        manzanoactiva = Manzano.objects.exclude(estado='True')
        context["manzano_count"] = manzanoactiva
        context["list_manzano"] = manzanotodo
        context['fields'] = MANZANO_FIELDS
        return context