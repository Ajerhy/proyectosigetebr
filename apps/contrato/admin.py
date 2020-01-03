from django.contrib import admin
from .models import Persona
from .models import Grupo
from .models import Cliente
from .models import Referenciacelular
from .models import Contrato

from .models import Moneda
from .models import Banco
from .models import Cuenta
from .models import Urbanizacion

from .models import Propietaria
from .models import Notaria


class lotesInlines(admin.TabularInline):
    model = Contrato.lotes.through

class LoteAdmin(admin.ModelAdmin):
    inlines = [
        lotesInlines,
    ]
class ContratoAdmin(admin.ModelAdmin):
    inlines = [
        lotesInlines,
    ]
    exclude = ('lotes',)

admin.site.register(Persona)
admin.site.register(Grupo)
admin.site.register(Cliente)
admin.site.register(Referenciacelular)
admin.site.register(Contrato,ContratoAdmin)
admin.site.register(Urbanizacion)
admin.site.register(Notaria)
admin.site.register(Propietaria)
admin.site.register(Moneda)
admin.site.register(Banco)
admin.site.register(Cuenta)
