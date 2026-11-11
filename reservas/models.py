from django.core.validators import MinValueValidator
from django.db import models


class ActividadDeportiva(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=150)
    cupo = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "El cupo debe ser mayor que cero.")]
    )

    class Meta:
        verbose_name = "Actividad deportiva"
        verbose_name_plural = "Actividades deportivas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
