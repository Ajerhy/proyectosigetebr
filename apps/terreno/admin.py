from django.contrib import admin
from .models import Ubicacion
from .models import Lote
from .models import Manzano
from .models import Medida
from .models import Distrito
"""
class lotesInlines(admin.TabularInline):
    model = Manzano.lotes.through

class LoteAdmin(admin.ModelAdmin):
    inlines = [
        lotesInlines,
    ]

class ManzanoAdmin(admin.ModelAdmin):
    inlines = [
        lotesInlines,
    ]
    exclude = ('lotes',)
"""
admin.site.register(Ubicacion)
admin.site.register(Lote)
#admin.site.register(Manzano,ManzanoAdmin)
admin.site.register(Manzano)
admin.site.register(Medida)
admin.site.register(Distrito)
