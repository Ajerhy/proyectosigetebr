from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import json

from apps.contrato.models import Moneda
from apps.contrato.form.forms_moneda import MonedaForm,MoneyForm

from apps.usuario.templatetags.utils import get_ip

MONEDA_FIELDS = [
    {'string': 'N°'},
    {'string': 'Moneda'},
    {'string': 'Sigla'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class MonedaListarView(LoginRequiredMixin,generic.ListView):
class MonedaListarView(LoginRequiredMixin,TemplateView):
    login_url = 'usuario:index'
    model = Moneda
    template_name = "sigetebr/apps/contrato/moneda/listar.html"
    #context_object_name = "list_moneda"
    paginate_by = 5

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('moneda'):
                queryset = queryset.filter(nombremoneda__icontains=request_post.get('moneda'))
            if request_post.get('sigla'):
                queryset = queryset.filter(siglamoneda__icontains=request_post.get('sigla'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MonedaListarView, self).get_context_data(**kwargs)
        context["list_moneda"] = self.get_queryset()
        context['fields'] = MONEDA_FIELDS

        search = False
        if (
                self.request.POST.get('moneda') or
                self.request.POST.get('sigla')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class MonedaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Moneda
    template_name = "sigetebr/apps/contrato/moneda/form.html"
    context_object_name = "obj_moneda"
    form_class = MonedaForm
    success_url = reverse_lazy("contrato:listar_moneda")
    success_message = "Moneda Creado Exitosamente"

    def form_valid(self, form):
        moneda = form.save(commit=False)
        moneda.uc = self.request.user.id
        moneda.direccion_ip=get_ip(self.request)
        moneda.save()
        return super().form_valid(form)

class MonedaEditaView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Moneda
    template_name = "sigetebr/apps/contrato/moneda/form.html"
    context_object_name = "obj_moneda"
    form_class = MonedaForm
    success_url = reverse_lazy("contrato:listar_moneda")
    success_message = "Moneda Actualizada Satisfactoriamente"

    def form_valid(self, form):
        moneda = form.save(commit=False)
        moneda.um = self.request.user.id
        moneda.direccion_ip=get_ip(self.request)
        moneda.save()
        return super().form_valid(form)

class MonedaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Moneda
    template_name = 'sigetebr/apps/contrato/moneda/detalle.html'#url
    context_object_name = 'obj'

class MonedaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Moneda
    template_name= 'sigetebr/apps/contrato/moneda/eliminar.html'
    context_object_name='obj_moneda'
    success_url = reverse_lazy("contrato:listar_moneda")
    success_message="Moneda Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def monedadesactivar(request, id):
    moneda = Moneda.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/moneda/estado_desactivar.html'#url

    if not moneda:
        return redirect('contrato:listar_moneda')

    if request.method=='GET':
        contexto={'obj':moneda}

    if request.method=='POST':
        moneda.estado=False
        moneda.save()

        return redirect('contrato:listar_moneda')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def monedaactivar(request, id):
    moneda = Moneda.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/moneda/estado_activar.html'#url

    if not moneda:
        return redirect('contrato:listar_moneda')

    if request.method=='GET':
        contexto={'obj':moneda}

    if request.method=='POST':
        moneda.estado=True
        moneda.save()
        return redirect('contrato:listar_moneda')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_moneda(request, pk):
    moneda = get_object_or_404(Moneda, pk=pk)
    if moneda.estado:
        moneda.estado = False
        messages.error(request, "Moneda Desactivada")
    else:
        moneda.estado = True
        messages.success(request, "Moneda Activada")
    moneda.um = request.user.id
    moneda.save()
    return redirect('contrato:listar_moneda')




def money(request):
    template_name = 'sigetebr/apps/contrato/moneda/form.html'
    if request.method == 'POST':

        form = MoneyForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'La Moneda Creada Exitosamente!')
            return redirect('contrato:listar_moneda')
        else:
            messages.warning(request, form.errors)

    else:
        form = MoneyForm()
        return render(request,template_name,{'form': form})
        #return render(request, , {'form': form})
