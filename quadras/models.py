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
