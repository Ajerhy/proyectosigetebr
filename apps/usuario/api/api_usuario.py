from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,Http404)
from rest_framework import status

from apps.usuario.api.serializers_usuario import Usuario1Serializer
from apps.usuario.models import Usuario

class UsuariosListarAPI(APIView):
    # poner autenticacion
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = Usuario.objects.all()
        serializer = Usuario1Serializer(users, many=True)
        serialized_users = serializer.data  # lista de diccionarios
        return Response(serialized_users)

    def post(self, request):
        serializer = Usuario1Serializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosDetalleAPI(APIView):
    #poner autenticacion
    permission_classes = (IsAuthenticated,)

    # Buscar el Objeto
    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    # Detalle
    def get(self, request, pk):
        user = get_object_or_404(Usuario, pk=pk)
        serializer = Usuario1Serializer(user)
        return Response(serializer.data)

    # Actualizar
    def put(self, request, pk):
        user = get_object_or_404(Usuario, pk=pk)
        serializer = Usuario1Serializer(instance=user, data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar
    def delete(self, request, pk):
        user = get_object_or_404(Usuario, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




from rest_framework.pagination import PageNumberPagination
from apps.usuario.permissions import UsuarioPemission
from rest_framework.viewsets import ViewSet

class UsuarioViewSet(ViewSet):
    permission_classes = (UsuarioPemission,)

    def list(self, request):
        self.check_permissions(request)
        # instancion paginador
        paginator = PageNumberPagination()
        users = Usuario.objects.all()
        # paginar el queryset
        paginator.paginate_queryset(users, request)
        serializer = Usuario1Serializer(users, many=True)
        serialized_users = serializer.data  # lista de diccionarios
        # devolver respuesta paginada
        return paginator.get_paginated_response(serialized_users)

    def create(self, request):
        self.check_permissions(request)
        serializer = Usuario1Serializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(Usuario, pk=pk)
        self.check_object_permissions(request, user)
        serializer = Usuario1Serializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(Usuario, pk=pk)
        self.check_object_permissions(request, user)
        serializer = Usuario1Serializer(instance=user, data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(Usuario, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)