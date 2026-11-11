from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("actividades/", views.lista_actividades, name="lista_actividades"),
    path("actividades/agregar/", views.agregar_actividad, name="agregar_actividad"),
    path("actividades/<int:id>/", views.detalle_actividad, name="detalle_actividad"),
]
