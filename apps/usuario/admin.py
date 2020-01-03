from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .models import Perfil
"""
class PersonalizadaUserAdmin(UserAdmin):
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'fields': ('usuario', 'password1', 'password2'),
        }),)
    list_display = ('usuario', 'email', 'is_active', 'is_staff')
    # 'password',
    search_fields = ('usuario',)

    ordering = ('usuario',)

    filter_horizontal = ()
    # filter_vertical = ()
admin.site.register(Usuario, PersonalizadaUserAdmin)
"""
class PersonalizadaPerfilAdmin(UserAdmin):
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'fields': ('usuario', 'password1', 'password2'),
        }),)
    list_display = ('usuario', 'email', 'roles','is_active','is_superuser', 'estado')
    # 'password',
    search_fields = ('usuario',)

    ordering = ('usuario',)

    filter_horizontal = ()
admin.site.register(Perfil, PersonalizadaPerfilAdmin)