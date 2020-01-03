from django.conf.urls import url, include
from django.urls import path
from apps.usuario.api.api_usuario import UsuarioViewSet
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()
router.register('usuario', UsuarioViewSet, base_name='usuario')
#router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    # API URLs
    path('1.0/', include(router.urls)),
]

"""
urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),
]
"""
