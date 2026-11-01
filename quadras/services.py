"""servicos relacionados ao cadastro de quadras."""
import datetime

from django.core.exceptions import ValidationError

from .models import Quadra



def cadastrar_quadra(nome: str, tipo: str, horario_abertura: datetime.time, horario_fechamento: datetime.time, dias_funcionamento: list[str]) -> Quadra:
    """valida os dados e salva uma nova quadra no banco."""
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

    if Quadra.objects.filter(nome__iexact=nome).exists():
        raise ValidationError({"nome": "Já existe uma quadra com este nome."})

    return Quadra.objects.create(nome=nome, tipo=tipo, horario_abertura=horario_abertura, horario_fechamento=horario_fechamento, dias_funcionamento=dias_validos)
