"""Operações seguras para criação de usuários."""
from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):
    """Cria usuários normalizando o e-mail e aplicando hash à senha."""

    use_in_migrations = True

    def create_user(self, email: str, nome: str, password: str | None = None, **extra_fields):
        if not email or not email.strip():
            raise ValueError("O e-mail é obrigatório.")
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        if not password:
            raise ValueError("A senha é obrigatória.")

        email_normalizado = self.normalize_email(email).strip().lower()
        usuario = self.model(
            email=email_normalizado,
            nome=nome.strip(),
            **extra_fields,
        )
        # Nunca persista a senha recebida em texto puro.
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(
        self,
        email: str,
        nome: str,
        password: str | None = None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Um superusuário precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Um superusuário precisa ter is_superuser=True.")

        return self.create_user(email, nome, password, **extra_fields)
