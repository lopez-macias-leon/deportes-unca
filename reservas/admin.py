from django.contrib import admin

from .models import ActividadDeportiva

admin.site.site_header = "Deportes UNCA - Administración"
admin.site.site_title = "Deportes UNCA"
admin.site.index_title = "Panel de gestión"


@admin.register(ActividadDeportiva)
class ActividadDeportivaAdmin(admin.ModelAdmin):
    # Columnas que se ven en el listado
    list_display = ("id", "nombre", "lugar", "cupo")
    # Campos por los que busca la barra de búsqueda
    search_fields = ("nombre", "lugar", "descripcion")
    # Extras: filtro lateral, enlaces, orden y paginación
    list_filter = ("lugar",)
    list_display_links = ("id", "nombre")
    ordering = ("nombre",)
    list_per_page = 20
