from django.db import models


class ActividadDeportiva(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=150)
    cupo = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Actividad deportiva"
        verbose_name_plural = "Actividades deportivas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
