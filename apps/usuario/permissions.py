from rest_framework.permissions import BasePermission


class UsuarioPemission(BasePermission):
    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para
        realizar la acción (GET, POST, PUT o DELETE)
        """
        # si quiere crear un usuario, sea quien sea, debe poder crearlo
        if request.method == "POST":
            return True
        # si es superuser, puede hacer lo que quiera
        elif request.user.is_superuser:
            return True
        # si no es POST (es GET, PUT o DELETE), el usuario no es superuser
        # y la petición va a la vista de detalle, entonces lo permitimos
        # para tomar la decisión en el método has_object_permission
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        # si la petición es un GET de listado, no lo permitimos (porque si llega
        # aquí, el usuario no es supeuser y sólo pueden los superuser)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para
        realizar la acción (GET, PUT o DELETE) sobre el objeto obj
        """
        return request.user.is_superuser or request.user == obj