"""Formulários relacionados ao cadastro de usuários."""
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario


class CadastroUsuarioForm(forms.Form):
    """Valida os dados enviados pela tela de cadastro."""

    nome = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "placeholder": "Digite seu nome completo",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "voce@exemplo.com",
            }
        ),
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Crie uma senha",
            }
        ),
        help_text="A senha deve atender aos critérios de segurança do sistema.",
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Digite a senha novamente",
            }
        ),
    )

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("O nome é obrigatório.")
        return nome

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Já existe uma conta cadastrada com este e-mail."
            )
        return email

    def clean_senha(self):
        senha = self.cleaned_data["senha"]
        try:
            validate_password(senha)
        except ValidationError as erro:
            raise forms.ValidationError(erro.messages) from erro
        return senha

    def clean(self):
        dados = super().clean()
        senha = dados.get("senha")
        confirmar_senha = dados.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas não coincidem.")
        return dados
