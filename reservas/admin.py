from django.contrib import admin

from .models import ActividadDeportiva, Horario, Inscripcion


@admin.register(ActividadDeportiva)
class ActividadDeportivaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lugar", "cupo")
    search_fields = ("nombre", "lugar")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("actividad", "dia", "hora_inicio", "hora_fin")
    list_filter = ("actividad", "dia")


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "dni", "horario", "estado", "fecha_inscripcion")
    list_filter = ("estado", "horario__actividad")
    search_fields = ("apellido", "nombre", "dni")
