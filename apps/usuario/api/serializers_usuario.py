from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
#from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.usuario.models import Usuario

class UsuarioSerializer(ModelSerializer):
	class Meta:
		model = Usuario
		fields = ('id','usuario','email', 'nombre')

"""
class PerfilSerializer(ModelSerializer):
	usuario = UsuarioSerializer(read_only=True)
	class Meta:
		model = Perfil
		fields = ('id','phone', 'usuario')
"""

class Usuario1Serializer(serializers.Serializer):
	id = serializers.ReadOnlyField()  # read only
	nombre = serializers.CharField()
	apellido = serializers.CharField()
	usuario = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField()

	def create(self, validated_data):
		"""
        Crea una instancia de un objeto User a partir de los datos de
        validated_data que contiene valores deserializados.
        """
		instance = Usuario()
		return self.update(instance, validated_data)

	def update(self, instance, validated_data):
		"""
        Crea una instancia de un objeto User a partir de los datos de
        validated_data que contiene valores deserializados.
        """
		instance.nombre = validated_data.get('nombre')
		instance.apellido = validated_data.get('apellido')
		instance.usuario = validated_data.get('usuario')
		instance.email = validated_data.get('email')
		instance.set_password(validated_data.get('password'))
		instance.save()
		return instance

	def validate_usuario(self, data):
		"""
        Valida si existe un usuario con ese username
        """
		user = Usuario.objects.filter(usuario=data)
		# Si estoy creando (no hay instancia) comprobar si hay usuarios con ese
		# username
		if not self.instance and len(user) != 0:
			raise ValidationError(u"Ya existe un usuario con ese usuario")
		# Si estoy actualizando (hay instancia) y estamos cambiando el username
		# y existen usuarios con el nuevo username
		elif self.instance.usuario != data and len(user) != 0:
			raise ValidationError(u"Ya existe un usuario con ese usuario")
		else:
			return data
