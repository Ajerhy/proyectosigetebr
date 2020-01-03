from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView,ListView)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from apps.usuario.templatetags.utils import get_ip
from apps.contrato.models import Persona
from apps.contrato.form.forms_persona import PersonaForm
from django.db.models import Q

#class PersonaListarView(LoginRequiredMixin,generic.ListView):
"""
class PersonaListarView(LoginRequiredMixin,TemplateView):
    model = Persona
    template_name ="sigetebr/apps/contrato/persona/listar.html"
    #context_object_name = "list_persona"
    #paginate_by = 5
    login_url = 'usuario:index'

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        print(request_post,"Persona")
        if request_post:
            if request_post.get('nombre'):
                queryset = queryset.filter(
                    nombrepersona__icontains=request_post.get('nombre'))
            if request_post.get('paterno'):
                queryset = queryset.filter(
                    paternopersona__icontains=request_post.get('paterno'))
            if request_post.get('materno'):
                queryset = queryset.filter(
                    maternopersona__icontains=request_post.get('materno'))
            if request_post.get('ci'):
                queryset = queryset.filter(
                    cipersona__icontains=request_post.get('ci'))
        print(queryset, "Resultado")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PersonaListarView, self).get_context_data(**kwargs)
        #Liminar Cagar de Lista Registros .order_by('-id')[:250]
        context["list_persona"] = self.get_queryset().order_by('-id')[:250]

        #context["persona_count"] = self.get_queryset().count()
        context["persona_count"] = self.model.objects.exclude(estado='False')

        context["per_page"] = self.request.POST.get('per_page')

        search = False
        if (
                self.request.POST.get('nombre') or
                self.request.POST.get('paterno') or
                self.request.POST.get('materno') or
                self.request.POST.get('ci')
        ):
            search = True
        context["search"] = search

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
"""
PERSONA_FIELDS = [
    {'string': 'N°'},
    {'string': 'Nombre'},
    {'string': 'Paterno'},
    {'string': 'Materno'},
    {'string': 'Ci'},
    {'string': 'Genero'},
    {'string': 'Estado'},
    {'string': 'Acciones'},
]

#class PersonaListarView(LoginRequiredMixin,generic.ListView):
class PersonaListarView(LoginRequiredMixin,TemplateView):
    template_name = 'sigetebr/apps/contrato/persona/listar.html'
    login_url = 'usuario:index'

    def get_context_data(self, **kwargs):
        context = super(PersonaListarView, self).get_context_data(**kwargs)
        personatodo = Persona.objects.all()
        personaactiva = Persona.objects.exclude(estado='True')
        context["persona_count"] = personaactiva
        context["list_persona"] = personatodo
        context['fields'] = PERSONA_FIELDS
        return context

class PersonaCrearView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Persona
    template_name = "sigetebr/apps/contrato/persona/form.html"
    context_object_name = "obj_persona"
    form_class = PersonaForm
    success_url = reverse_lazy("contrato:listar_persona")
    success_message = "Persona Creada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        persona = form.save(commit=False)
        persona.uc = self.request.user.id
        persona.direccion_ip=get_ip(self.request)
        persona.save()
        return super().form_valid(form)

class PersonaEditarView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Persona
    template_name = "sigetebr/apps/contrato/persona/form.html"
    form_class = PersonaForm
    context_object_name = "obj_persona"
    success_url = reverse_lazy("contrato:listar_persona")
    success_message = "Persona Modificada Exitosamente"
    login_url = 'usuario:index'

    def form_valid(self, form):
        persona = form.save(commit=False)
        persona.um = self.request.user.id
        persona.direccion_ip=get_ip(self.request)
        persona.save()
        return super().form_valid(form)

class PersonaEliminarView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    login_url = 'usuario:index'
    model = Persona
    template_name= 'sigetebr/apps/contrato/persona/eliminar.html'
    context_object_name='obj_persona'
    success_url = reverse_lazy("contrato:listar_persona")
    success_message="Persona Eliminada Exitosamente"

class PersonaDetalleView(LoginRequiredMixin,DetailView):
    login_url = 'usuario:index'
    model = Persona
    template_name = 'sigetebr/apps/contrato/persona/detalle.html'#url
    context_object_name = 'obj'

@login_required(login_url='usuario:index')
def cambiar_estado_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if persona.estado:
        persona.estado = False
        messages.error(request, "Persona Desactivada")
    else:
        persona.estado = True
        messages.success(request, "Persona Activada")
    #persona.um = request.user.id
    #persona.direccion_ip = get_ip(request)
    persona.save()
    return redirect('contrato:listar_persona')

@login_required(login_url='usuario:index')
def personadesactivar(request, id):
    persona = Persona.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/persona/estado_desactivar.html'#url

    if not persona:
        return redirect('contrato:listar_persona')

    if request.method=='GET':
        contexto={'obj':persona}

    if request.method=='POST':
        persona.estado=False
        persona.save()
        messages.error(request, "Persona Desactivada")
        return redirect('contrato:listar_persona')

    return render(request,template_name,contexto)

@login_required(login_url='usuario:index')
def personaactivar(request, id):
    persona = Persona.objects.filter(pk=id).first()
    contexto={}
    template_name = 'sigetebr/apps/contrato/persona/estado_activar.html'#url

    if not persona:
        return redirect('contrato:listar_persona')

    if request.method=='GET':
        contexto={'obj':persona}

    if request.method=='POST':
        persona.estado=True
        persona.save()
        messages.success(request, "Persona Activada")
        return redirect('contrato:listar_persona')

    return render(request,template_name,contexto)
