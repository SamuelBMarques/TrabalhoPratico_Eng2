"""Serviços relacionados ao cadastro de usuários."""
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .models import Usuario


@transaction.atomic
def cadastrar_usuario(nome: str, email: str, senha: str) -> Usuario:
    """
    Valida os dados básicos e persiste um usuário no banco.

    A senha é encaminhada ao manager do modelo, que usa set_password()
    para armazenar somente o hash da senha.
    """
    nome = (nome or "").strip()
    email = (email or "").strip().lower()

    if not nome:
        raise ValidationError({"nome": "O nome é obrigatório."})

    if not email:
        raise ValidationError({"email": "O e-mail é obrigatório."})

    if not senha:
        raise ValidationError({"senha": "A senha é obrigatória."})

    if Usuario.objects.filter(email__iexact=email).exists():
        raise ValidationError({"email": "Já existe uma conta com este e-mail."})

    try:
        return Usuario.objects.create_user(
            nome=nome,
            email=email,
            password=senha,
        )
    except IntegrityError as exc:
        # A restrição UNIQUE no banco também protege contra cadastros simultâneos.
        raise ValidationError(
            {"email": "Já existe uma conta com este e-mail."}
        ) from exc