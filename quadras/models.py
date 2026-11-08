import datetime

from django.db import models


class Quadra (models.Model):
    DIAS_SEMANA = [
        ("seg", "Segunda"),
        ("ter", "Terça"),
        ("qua", "Quarta"),
        ("qui", "Quinta"),
        ("sex", "Sexta"),
        ("sab", "Sábado"),
        ("dom", "Domingo"),
    ]

    nome = models.CharField(max_length = 150)
    tipo = models.CharField(max_length = 150)
    ativa = models.BooleanField(default = True)
    horario_abertura = models.TimeField(default = datetime.time(8, 0))
    horario_fechamento = models.TimeField(default = datetime.time(22, 0))
    # lista com os codigos dos dias em que a quadra abre, ex: seg, qua
    dias_funcionamento = models.JSONField(default = list)

    def __str__(self):
        return self.nome

    @property
    def dias_legiveis(self) -> list[str]:
        """nomes dos dias de funcionamento, na ordem da semana."""
        return [nome for codigo, nome in self.DIAS_SEMANA if codigo in self.dias_funcionamento]


class HorarioFuncionamento(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name="horarios_funcionamento")
    dia_semana = models.CharField(max_length=3, choices=Quadra.DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["dia_semana", "hora_inicio"]
        constraints = [
            models.CheckConstraint(condition=models.Q(hora_fim__gt=models.F("hora_inicio")), name="horario_fim_depois_do_inicio"),
        ]

    def __str__(self):
        return f"{self.quadra} - {self.get_dia_semana_display()} {self.hora_inicio:%H:%M} às {self.hora_fim:%H:%M}"
