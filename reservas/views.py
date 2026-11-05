"""views relacionadas a consulta de horarios e a criacao de reservas."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from quadras.models import Quadra

from .forms import ConsultaHorariosForm, ReservaForm
from .services import criar_reserva, listar_horarios_disponiveis


def horarios(request, quadra_id):
    """mostra os horarios livres de uma quadra na data escolhida (hoje, se nenhuma for informada)."""
    quadra = get_object_or_404(Quadra, pk=quadra_id)
    form = ConsultaHorariosForm(request.GET or {"data": timezone.localdate()})

    data = None
    horarios_livres = []
    if form.is_valid():
        data = form.cleaned_data["data"]
        horarios_livres = listar_horarios_disponiveis(quadra, data)

    return render(request, "reservas/horarios.html", {"quadra": quadra, "form": form, "data": data, "horarios": horarios_livres})


@login_required
def reservar(request, quadra_id):
    """cria a reserva do usuario logado e volta para os horarios da mesma data."""
    quadra = get_object_or_404(Quadra, pk=quadra_id)
    url_horarios = reverse("reservas:horarios", args=[quadra.pk])

    # quem caiu no login no meio de uma reserva volta pra ca por GET
    if request.method != "POST":
        return redirect(url_horarios)

    form = ReservaForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Não foi possível reservar. Escolha um horário da lista.")
        return redirect(url_horarios)

    data = form.cleaned_data["data"]
    try:
        reserva = criar_reserva(request.user, quadra, data, form.cleaned_data["hora_inicio"])
    except ValidationError as erro:
        messages.error(request, erro.messages[0])
    else:
        messages.success(request, f"Reserva confirmada: {quadra.nome}, {reserva.data:%d/%m/%Y}, das {reserva.hora_inicio:%H:%M} às {reserva.hora_fim:%H:%M}.")
    return redirect(f"{url_horarios}?data={data.isoformat()}")
