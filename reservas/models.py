"""modelos dos periodos que ocupam uma quadra: reservas e bloqueios."""
from django.conf import settings
from django.db import models
from django.db.models import F, Q

from quadras.models import Quadra


class Reserva(models.Model):
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    STATUS = [
        (CONFIRMADA, "Confirmada"),
        (CANCELADA, "Cancelada"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservas")
    # PROTECT porque o historico de reservas nao pode sumir junto com a quadra
    quadra = models.ForeignKey(Quadra, on_delete=models.PROTECT, related_name="reservas")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS, default=CONFIRMADA)

    class Meta:
        ordering = ["data", "hora_inicio"]
        constraints = [
            models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="reserva_fim_depois_do_inicio"),
            # garantia no banco: duas pessoas reservando ao mesmo tempo nao conseguem o mesmo horario
            models.UniqueConstraint(fields=["quadra", "data", "hora_inicio"], condition=Q(status="confirmada"), name="reserva_confirmada_unica"),
        ]

    def __str__(self):
        return f"{self.quadra} em {self.data:%d/%m/%Y} das {self.hora_inicio:%H:%M} às {self.hora_fim:%H:%M}"


class Bloqueio(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name="bloqueios")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        ordering = ["data", "hora_inicio"]
        constraints = [
            models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="bloqueio_fim_depois_do_inicio"),
        ]

    def __str__(self):
        return f"{self.quadra} em {self.data:%d/%m/%Y} das {self.hora_inicio:%H:%M} às {self.hora_fim:%H:%M}"
