from django.db import models


class ActividadDeportiva(models.Model):
    """Actividades deportivas que ofrece la plataforma Deportes Unca."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    lugar = models.CharField(max_length=150)
    cupo = models.PositiveIntegerField()

    class Meta:
        verbose_name = "actividad deportiva"
        verbose_name_plural = "actividades deportivas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    """Horarios disponibles para cada actividad deportiva.

    Una actividad puede tener varios horarios (ForeignKey en el lado "muchos").
    """

    DIAS = [
        ("LUN", "Lunes"),
        ("MAR", "Martes"),
        ("MIE", "Miércoles"),
        ("JUE", "Jueves"),
        ("VIE", "Viernes"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]

    actividad = models.ForeignKey(
        ActividadDeportiva,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    dia = models.CharField(max_length=3, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ["actividad", "dia", "hora_inicio"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(hora_fin__gt=models.F("hora_inicio")),
                name="hora_fin_posterior_a_hora_inicio",
            ),
        ]

    def __str__(self):
        return (
            f"{self.actividad} - {self.get_dia_display()} "
            f"{self.hora_inicio:%H:%M} a {self.hora_fin:%H:%M}"
        )


class Inscripcion(models.Model):
    """Inscripción de una persona a un horario de una actividad deportiva."""

    ACTIVA = "ACTIVA"
    CANCELADA = "CANCELADA"
    ESTADOS = [
        (ACTIVA, "Activa"),
        (CANCELADA, "Cancelada"),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVA)
    horario = models.ForeignKey(
        Horario,
        on_delete=models.PROTECT,
        related_name="inscripciones",
    )

    class Meta:
        verbose_name = "inscripción"
        verbose_name_plural = "inscripciones"
        ordering = ["-fecha_inscripcion", "apellido"]
        constraints = [
            # Una misma persona no puede inscribirse dos veces al mismo horario.
            models.UniqueConstraint(
                fields=["dni", "horario"],
                name="inscripcion_unica_por_horario",
            ),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni}) - {self.horario}"
