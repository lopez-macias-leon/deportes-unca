from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "reservas"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="reservas:lista_actividades")),
    path("actividades/", views.lista_actividades, name="lista_actividades"),
    path("actividades/agregar/", views.agregar_actividad, name="agregar_actividad"),
    path("actividades/<int:id>/", views.detalle_actividad, name="detalle_actividad"),
    path("actividades/<int:id>/editar/", views.editar_actividad, name="editar_actividad"),
    path("actividades/<int:id>/eliminar/", views.eliminar_actividad, name="eliminar_actividad"),
]
