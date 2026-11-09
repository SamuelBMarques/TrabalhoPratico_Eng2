"""servicos relacionados ao cadastro, edicao e desativacao de quadras."""
import datetime

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db.models.functions import Lower

from .models import HorarioFuncionamento, Quadra



def validar_dados_quadra(nome: str, tipo: str, horario_abertura: datetime.time, horario_fechamento: datetime.time, dias_funcionamento: list[str], quadra_id: int | None = None) -> dict:
    """valida e limpa os dados de uma quadra, usado no cadastro e na edicao."""
    nome = (nome or "").strip()
    tipo = (tipo or "").strip()

    if not nome:
        raise ValidationError({"nome": "O nome é obrigatório."})

    if not tipo:
        raise ValidationError({"tipo": "O tipo é obrigatório."})

    if not horario_abertura or not horario_fechamento:
        raise ValidationError({"horario_abertura": "Informe os horários de funcionamento."})

    if horario_fechamento <= horario_abertura:
        raise ValidationError({"horario_fechamento": "O horário de fechamento deve ser depois da abertura."})

    # mantem so os codigos validos, na ordem da semana
    dias_validos = [codigo for codigo, _ in Quadra.DIAS_SEMANA if codigo in (dias_funcionamento or [])]
    if not dias_validos:
        raise ValidationError({"dias_funcionamento": "Escolha pelo menos um dia."})

    # na edicao a propria quadra nao conta como nome repetido
    repetidas = Quadra.objects.filter(nome__iexact=nome)
    if quadra_id is not None:
        repetidas = repetidas.exclude(pk=quadra_id)
    if repetidas.exists():
        raise ValidationError({"nome": "Já existe uma quadra com este nome."})

    return {"nome": nome, "tipo": tipo, "horario_abertura": horario_abertura, "horario_fechamento": horario_fechamento, "dias_funcionamento": dias_validos}


def cadastrar_quadra(nome: str, tipo: str, horario_abertura: datetime.time, horario_fechamento: datetime.time, dias_funcionamento: list[str]) -> Quadra:
    """valida os dados e salva uma nova quadra no banco."""
    dados = validar_dados_quadra(nome, tipo, horario_abertura, horario_fechamento, dias_funcionamento)
    return Quadra.objects.create(**dados)


def editar_quadra(quadra: Quadra, nome: str, tipo: str, horario_abertura: datetime.time, horario_fechamento: datetime.time, dias_funcionamento: list[str]) -> Quadra:
    """valida os dados novos e atualiza uma quadra que ja existe."""
    dados = validar_dados_quadra(nome, tipo, horario_abertura, horario_fechamento, dias_funcionamento, quadra.pk)
    for campo, valor in dados.items():
        setattr(quadra, campo, valor)
    quadra.save()
    return quadra


def desativar_quadra(quadra: Quadra) -> Quadra:
    """tira a quadra de uso sem apagar do banco, assim o historico de reservas continua."""
    if not quadra.ativa:
        raise ValidationError("A quadra já está desativada.")
    quadra.ativa = False
    quadra.save(update_fields=["ativa"])
    return quadra


def reativar_quadra(quadra: Quadra) -> Quadra:
    """coloca de volta em uso uma quadra que estava desativada."""
    if quadra.ativa:
        raise ValidationError("A quadra já está ativa.")
    quadra.ativa = True
    quadra.save(update_fields=["ativa"])
    return quadra


def listar_quadras() -> QuerySet[Quadra]:
    """retorna todas as quadras: primeiro as ativas, depois em ordem alfabetica."""
    return Quadra.objects.order_by("-ativa", Lower("nome"))


def cadastrar_horario(quadra: Quadra, dia_semana: str, hora_inicio: datetime.time, hora_fim: datetime.time, ativo: bool = True) -> HorarioFuncionamento:
    if hora_fim <= hora_inicio:
        raise ValidationError({"hora_fim": "O horário de fechamento deve ser depois da abertura."})
    return HorarioFuncionamento.objects.create(
        quadra=quadra,
        dia_semana=dia_semana,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        ativo=ativo,
    )


def editar_horario(horario: HorarioFuncionamento, dia_semana: str, hora_inicio: datetime.time, hora_fim: datetime.time, ativo: bool = True) -> HorarioFuncionamento:
    if hora_fim <= hora_inicio:
        raise ValidationError({"hora_fim": "O horário de fechamento deve ser depois da abertura."})
    horario.dia_semana = dia_semana
    horario.hora_inicio = hora_inicio
    horario.hora_fim = hora_fim
    horario.ativo = ativo
    horario.save()
    return horario
