from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip

from apps.terreno.models import Medida
from apps.terreno.form.forms_medida import MedidaForm

from django.db.models import Q

MEDIDA_FIELDS = [
    {'string': 'N°', 'modelos': 'forloop.counter'},
    {'string': 'Largo', 'modelos': 'largomedida'},
    {'string': 'Ancho', 'modelos': 'anchomedida'},
    {'string': 'Superficie', 'modelos': 'superficietotal'},
    {'string': 'Estado', 'modelos': 'estado'},
    {'string': 'Acciones', 'modelos': 'id'},
]

#class MedidaListarView(LoginRequiredMixin,ListView):
class MedidaListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/terreno/medida/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(MedidaListarView, self).get_context_data(**kwargs)
        medidatodo = Medida.objects.all()
        medidaactiva = Medida.objects.exclude(estado='True')
        context["medida_count"] = medidaactiva
        context["list_medida"] =  medidatodo


        context['crear_medida_url'] = 'terreno:crear_medida'
        context['detalle_medida_url'] = 'terreno:crear_medida'

        context['fields'] = MEDIDA_FIELDS
        return context

class MedidaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Medida
    template_name = "sigetebr/apps/terreno/medida/form.html"
    context_object_name = "obj_medida"
    form_class = MedidaForm
    success_url = reverse_lazy("terreno:listar_medida")
    success_message = "Medida Creada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        persona = form.save(commit=False)
        persona.uc = self.request.user
        persona.direccion_ip=get_ip(self.request)
        persona.save()
        return super().form_valid(form)

class MedidaEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Medida
    template_name = "sigetebr/apps/terreno/medida/form.html"
    form_class = MedidaForm
    context_object_name = "obj_medida"
    success_url = reverse_lazy("terreno:listar_medida")
    success_message = "Medida Modificada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        persona = form.save(commit=False)
        persona.um = self.request.user.id
        persona.direccion_ip=get_ip(self.request)
        persona.save()
        return super().form_valid(form)

class MedidaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Medida
    template_name = 'sigetebr/apps/terreno/medida/detalle.html'#url
    context_object_name = 'obj'

class MedidaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Medida
    template_name= 'sigetebr/apps/terreno/medida/eliminar.html'
    context_object_name='obj_medida'
    success_url = reverse_lazy("terreno:listar_medida")
    success_message="Medida Eliminada Exitosamente"

@login_required(login_url='usuario:index')
def medidadesactivar(request, id):
    medida = Medida.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/terreno/medida/estado_desactivar.html'#url

    if not medida:
        return redirect('terreno:listar_medida')

    if request.method=='GET':
        contexto={'obj':medida}

    if request.method=='POST':
        medida.estado=False
        medida.save()
        messages.error(request, "Medida Desactivada")
        return redirect('terreno:listar_medida')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def medidaactivar(request, id):
    medida = Medida.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/terreno/medida/estado_activar.html'#url

    if not medida:
        return redirect('terreno:listar_medida')

    if request.method=='GET':
        contexto={'obj':medida}

    if request.method=='POST':
        medida.estado=True
        medida.save()
        messages.success(request, "Medida Activada")
        return redirect('terreno:listar_medida')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def cambiar_estado_medida(request, pk):
    medida = get_object_or_404(Medida, pk=pk)
    if medida.estado:
        medida.estado = False
        messages.error(request, "Medida Desactivada")
    else:
        medida.estado = True
        messages.success(request, "Medida Activada")
    #persona.um = request.user.id
    #persona.direccion_ip = get_ip(request)
    medida.save()
    return redirect('terreno:listar_medida')
