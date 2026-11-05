from django.contrib import admin

from .models import Bloqueio, Reserva

# enquanto as telas de reserva (H05) e bloqueio (H13) nao existem, o admin permite registrar esses dados
admin.site.register(Reserva)
admin.site.register(Bloqueio)
