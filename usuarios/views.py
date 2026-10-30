"""Views relacionadas ao cadastro de usuários."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm
from .services import cadastrar_usuario


def cadastro(request):
    """Exibe e processa o formulário de criação de conta."""
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                cadastrar_usuario(
                    nome=form.cleaned_data["nome"],
                    email=form.cleaned_data["email"],
                    senha=form.cleaned_data["senha"],
                )
            except ValidationError as erro:
                if hasattr(erro, "message_dict"):
                    for campo, erros in erro.message_dict.items():
                        for mensagem in erros:
                            if campo in form.fields:
                                form.add_error(campo, mensagem)
                            else:
                                form.add_error(None, mensagem)
                else:
                    for mensagem in erro.messages:
                        form.add_error(None, mensagem)
            else:
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect("usuarios:cadastro")
    else:
        form = CadastroUsuarioForm()

    return render(request, "usuarios/cadastro.html", {"form": form})
