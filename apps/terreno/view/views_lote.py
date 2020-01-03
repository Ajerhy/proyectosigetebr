from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.terreno.models import Lote
from apps.contrato.form.forms_grupo import GrupoForm

from django.db.models import Q

LOTE_FIELDS = [
    {'string': 'N°'},
    {'string': 'Codigo'},
    {'string': 'Numero'},
    {'string': 'Sigla'},
    {'string': 'Superficie'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class LoteListarView(LoginRequiredMixin,generic.ListView):
class LoteListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/terreno/lote/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(LoteListarView, self).get_context_data(**kwargs)
        lotetodo = Lote.objects.all()
        loteactiva = Lote.objects.exclude(estado='True')
        context["lote_count"] = loteactiva
        context["list_lote"] = lotetodo
        context['fields'] = LOTE_FIELDS
        return context