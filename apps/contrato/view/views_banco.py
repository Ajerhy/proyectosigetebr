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

from apps.contrato.form.forms_banco import BancoForm
from apps.contrato.models import Banco

BANCO_FIELDS = [
    {'string': 'N°'},
    {'string': 'Banco'},
    {'string': 'Sigla'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class BancoListarView(LoginRequiredMixin,ListView):
class BancoListarView(LoginRequiredMixin, TemplateView):
    model = Banco
    template_name = "sigetebr/apps/contrato/banco/listar.html"
    #context_object_name = "list_banco"
    paginate_by = 10
    login_url = 'usuario:index'

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        print(request_post,"Banco")
        if request_post:
            if request_post.get('banco'):
                queryset = queryset.filter(
                    nombrebanco__icontains=request_post.get('banco'))
            if request_post.get('sigla'):
                queryset = queryset.filter(
                    siglabanco__icontains=request_post.get('sigla'))
        print(queryset, "Resultado")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BancoListarView,self).get_context_data(**kwargs)
        context["list_banco"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context['fields'] = BANCO_FIELDS

        search = False
        if (
                self.request.POST.get('banco') or
                self.request.POST.get('sigla')
        ):
            search = True
        context["search"] = search

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class BancoCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = 'usuario:index'
    model = Banco
    template_name = "sigetebr/apps/contrato/banco/form.html"
    context_object_name = "obj_banco"
    form_class = BancoForm
    success_url = reverse_lazy("contrato:listar_banco")
    success_message = "Banco Creado Exitosamente"

    def form_valid(self, form):
        banco = form.save(commit=False)
        banco.uc = self.request.user.id
        banco.direccion_ip=get_ip(self.request)
        banco.save()
        return super().form_valid(form)

class BancoEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Banco
    template_name = "sigetebr/apps/contrato/banco/form.html"
    context_object_name = "obj_banco"
    form_class = BancoForm
    success_url = reverse_lazy("contrato:listar_banco")
    success_message = "Banco Actualizado Satisfactoriamente"

    def form_valid(self, form):
        banco = form.save(commit=False)
        banco.um = self.request.user.id
        banco.direccion_ip=get_ip(self.request)
        banco.save()
        return super().form_valid(form)

class BancoDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Banco
    template_name = 'sigetebr/apps/contrato/banco/detalle.html'#url
    context_object_name = 'obj'

class BancoEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Banco
    template_name= 'sigetebr/apps/contrato/banco/eliminar.html'
    context_object_name='obj_banco'
    success_url = reverse_lazy("contrato:listar_banco")
    success_message="Banco Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def bancodesactivar(request, id):
    banco = Banco.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/banco/estado_desactivar.html'#url

    if not banco:
        return redirect('contrato:listar_banco')

    if request.method=='GET':
        contexto={'obj':banco}

    if request.method=='POST':
        banco.estado=False
        banco.save()
        messages.error(request, "Banco Desactivada")
        return redirect('contrato:listar_banco')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def bancoactivar(request, id):
    banco = Banco.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/banco/estado_activar.html'#url

    if not banco:
        return redirect('contrato:listar_banco')

    if request.method=='GET':
        contexto={'obj':banco}

    if request.method=='POST':
        banco.estado=True
        banco.save()
        messages.success(request, "Banco Activada")
        return redirect('contrato:listar_banco')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_banco(request, pk):
    banco = get_object_or_404(Banco, pk=pk)
    if banco.estado:
        banco.estado = False
        messages.error(request, "Banco Desactivada")
    else:
        banco.estado = True
        messages.success(request, "Banco Activada")
    banco.save()
    return redirect('contrato:listar_banco')
