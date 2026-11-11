from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ActividadDeportivaForm
from .models import ActividadDeportiva

# Seguridad: todas las vistas exigen usuario autenticado (login_required) y el
# permiso correspondiente a su rol (permission_required). Si el usuario no tiene
# el permiso se responde 403 - Prohibido.


@login_required
@permission_required("reservas.view_actividaddeportiva", raise_exception=True)
def lista_actividades(request):
    actividades = ActividadDeportiva.objects.all()
    return render(request, "reservas/lista_actividades.html", {"actividades": actividades})


@login_required
@permission_required("reservas.view_actividaddeportiva", raise_exception=True)
def detalle_actividad(request, id):
    actividad = get_object_or_404(ActividadDeportiva, pk=id)
    return render(request, "reservas/detalle_actividad.html", {"actividad": actividad})


@login_required
@permission_required("reservas.add_actividaddeportiva", raise_exception=True)
def agregar_actividad(request):
    if request.method == "POST":
        form = ActividadDeportivaForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f'La actividad "{actividad.nombre}" se registró correctamente.')
            return redirect("reservas:lista_actividades")
        messages.error(request, "Revisá los datos ingresados. Hay campos que necesitan corrección.")
    else:
        form = ActividadDeportivaForm()
    return render(request, "reservas/agregar_actividad.html", {"form": form, "titulo": "Registrar una nueva actividad deportiva"})


@login_required
@permission_required("reservas.change_actividaddeportiva", raise_exception=True)
def editar_actividad(request, id):
    actividad = get_object_or_404(ActividadDeportiva, pk=id)
    if request.method == "POST":
        form = ActividadDeportivaForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, f'La actividad "{actividad.nombre}" se actualizó correctamente.')
            return redirect("reservas:detalle_actividad", id=actividad.id)
        messages.error(request, "Revisá los datos ingresados. Hay campos que necesitan corrección.")
    else:
        form = ActividadDeportivaForm(instance=actividad)
    return render(request, "reservas/agregar_actividad.html", {"form": form, "titulo": f"Editar: {actividad.nombre}"})


@login_required
@permission_required("reservas.delete_actividaddeportiva", raise_exception=True)
@require_POST
def eliminar_actividad(request, id):
    actividad = get_object_or_404(ActividadDeportiva, pk=id)
    nombre = actividad.nombre
    actividad.delete()
    messages.success(request, f'La actividad "{nombre}" se eliminó.')
    return redirect("reservas:lista_actividades")
