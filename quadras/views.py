"""views relacionadas ao cadastro de quadras."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import CadastroQuadraForm
from .services import cadastrar_quadra


def cadastro(request):
    """exibe e processa o formulario de cadastro de quadra."""
    if request.method == "POST":
        form = CadastroQuadraForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            try:
                cadastrar_quadra(dados["nome"], dados["tipo"], dados["horario_abertura"], dados["horario_fechamento"], dados["dias_funcionamento"])
            except ValidationError as erro:
                for campo, erros in erro.message_dict.items():
                    for mensagem in erros:
                        form.add_error(campo, mensagem)
            else:
                messages.success(request, "Quadra cadastrada com sucesso!")
                return redirect("quadras:cadastro")
    else:
        form = CadastroQuadraForm()

    return render(request, "quadras/cadastro.html", {"form": form})
