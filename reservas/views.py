from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ActividadDeportivaForm
from .models import ActividadDeportiva


def agregar_actividad(request):
    if request.method == "POST":
        form = ActividadDeportivaForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(
                request,
                f'La actividad "{actividad.nombre}" se registró correctamente.'
            )
            return redirect("reservas:lista_actividades")
        messages.error(request, "Revisá los datos ingresados. Hay campos que necesitan corrección.")
    else:
        form = ActividadDeportivaForm()

    return render(
        request,
        "reservas/agregar_actividad.html",
        {"form": form},
    )


def lista_actividades(request):
    actividades = ActividadDeportiva.objects.all()
    return render(
        request,
        "reservas/lista_actividades.html",
        {"actividades": actividades},
    )


def detalle_actividad(request, id):
    actividad = get_object_or_404(ActividadDeportiva, pk=id)
    return render(
        request,
        "reservas/detalle_actividad.html",
        {"actividad": actividad},
    )
