"""servicos relacionados a consulta de horarios disponiveis e a criacao de reservas."""
import datetime
from typing import NamedTuple

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from quadras.models import Quadra

from .models import Bloqueio, Reserva

DURACAO_HORARIO = datetime.timedelta(hours=1)


class Horario(NamedTuple):
    inicio: datetime.time
    fim: datetime.time


def gerar_horarios_de_funcionamento(quadra: Quadra, data: datetime.date) -> list[Horario]:
    """divide o funcionamento do dia em horarios de 1 hora, a partir da abertura."""
    # weekday() comeca na segunda, mesma ordem de Quadra.DIAS_SEMANA
    codigo_do_dia = Quadra.DIAS_SEMANA[data.weekday()][0]
    if codigo_do_dia not in quadra.dias_funcionamento:
        return []

    horarios = []
    inicio = datetime.datetime.combine(data, quadra.horario_abertura)
    fechamento = datetime.datetime.combine(data, quadra.horario_fechamento)
    # um pedaco menor que 1 hora no fim do dia nao vira horario
    while inicio + DURACAO_HORARIO <= fechamento:
        fim = inicio + DURACAO_HORARIO
        horarios.append(Horario(inicio.time(), fim.time()))
        inicio = fim
    return horarios


def buscar_periodos_ocupados(quadra: Quadra, data: datetime.date, reserva_ignorada: Reserva | None = None) -> list[Horario]:
    """junta as reservas confirmadas e os bloqueios da quadra na data."""
    reservas = Reserva.objects.filter(quadra=quadra, data=data, status=Reserva.CONFIRMADA)
    if reserva_ignorada is not None:
        reservas = reservas.exclude(pk=reserva_ignorada.pk)
    bloqueios = Bloqueio.objects.filter(quadra=quadra, data=data)
    periodos = list(reservas.values_list("hora_inicio", "hora_fim")) + list(bloqueios.values_list("hora_inicio", "hora_fim"))
    return [Horario(inicio, fim) for inicio, fim in periodos]


def listar_horarios_disponiveis(
    quadra: Quadra,
    data: datetime.date,
    agora: datetime.datetime | None = None,
    reserva_ignorada: Reserva | None = None,
) -> list[Horario]:
    """retorna os horarios livres da quadra na data, sem os que ja passaram."""
    if not quadra.ativa:
        return []

    agora = agora or timezone.localtime()
    if data < agora.date():
        return []

    horarios = gerar_horarios_de_funcionamento(quadra, data)
    if data == agora.date():
        horarios = [horario for horario in horarios if horario.inicio > agora.time()]

    ocupados = buscar_periodos_ocupados(quadra, data, reserva_ignorada)
    return [
        horario for horario in horarios
        if not any(horario.inicio < ocupado.fim and ocupado.inicio < horario.fim for ocupado in ocupados)
    ]


def horario_esta_disponivel(
    quadra: Quadra,
    data: datetime.date,
    inicio: datetime.time,
    fim: datetime.time,
    reserva_ignorada: Reserva | None = None,
) -> bool:
    """confere de novo um horario escolhido, usado pela criacao da reserva antes de salvar."""
    return Horario(inicio, fim) in listar_horarios_disponiveis(quadra, data, reserva_ignorada=reserva_ignorada)


def criar_reserva(usuario, quadra: Quadra, data: datetime.date, inicio: datetime.time) -> Reserva:
    """valida a disponibilidade e registra a reserva do usuario."""
    fim = (datetime.datetime.combine(data, inicio) + DURACAO_HORARIO).time()
    erro = ValidationError("Esse horário não está mais disponível. Escolha outro.")

    if not horario_esta_disponivel(quadra, data, inicio, fim):
        raise erro

    try:
        return Reserva.objects.create(usuario=usuario, quadra=quadra, data=data, hora_inicio=inicio, hora_fim=fim)
    except IntegrityError:
        # outra pessoa reservou o mesmo horario entre a verificacao e o registro
        raise erro from None


def cancelar_reserva(reserva: Reserva) -> Reserva:
    """cancela uma reserva confirmada e libera o horario."""
    if reserva.status != Reserva.CONFIRMADA:
        raise ValidationError("Essa reserva já está cancelada.")

    reserva.status = Reserva.CANCELADA
    reserva.save(update_fields=["status"])
    return reserva


def alterar_reserva(reserva: Reserva, data: datetime.date, inicio: datetime.time) -> Reserva:
    """altera data e inicio de uma reserva sem perder a reserva original em caso de erro."""
    fim = (datetime.datetime.combine(data, inicio) + DURACAO_HORARIO).time()
    erro = ValidationError("Esse horário não está mais disponível. Escolha outro.")

    if reserva.status != Reserva.CONFIRMADA or not horario_esta_disponivel(reserva.quadra, data, inicio, fim, reserva):
        raise erro

    reserva.data = data
    reserva.hora_inicio = inicio
    reserva.hora_fim = fim
    try:
        reserva.save(update_fields=["data", "hora_inicio", "hora_fim"])
    except IntegrityError:
        raise erro from None
    return reserva
