from django import forms
from .models import ActividadDeportiva


class ActividadDeportivaForm(forms.ModelForm):
    class Meta:
        model = ActividadDeportiva
        fields = ["nombre", "descripcion", "lugar", "cupo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej.: Fútbol"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "placeholder": "Descripción de la actividad"}),
            "lugar": forms.TextInput(attrs={"placeholder": "Ej.: Polideportivo central"}),
            "cupo": forms.NumberInput(attrs={"min": 1, "placeholder": "Cantidad de participantes"}),
        }

    def clean_cupo(self):
        cupo = self.cleaned_data["cupo"]
        if cupo < 1:
            raise forms.ValidationError("El cupo debe ser mayor que cero.")
        return cupo
