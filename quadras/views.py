"""views relacionadas ao cadastro, edicao e desativacao de quadras."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroQuadraForm
from .models import Quadra
from .services import cadastrar_quadra, desativar_quadra, editar_quadra, reativar_quadra
from .services import listar_quadras


def mostrar_erros_no_form(form, erro):
    """coloca os erros vindos do service embaixo dos campos certos do form."""
    for campo, erros in erro.message_dict.items():
        for mensagem in erros:
            form.add_error(campo, mensagem)


def cadastro(request):
    """exibe e processa o formulario de cadastro de quadra."""
    if request.method == "POST":
        form = CadastroQuadraForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            try:
                cadastrar_quadra(dados["nome"], dados["tipo"], dados["horario_abertura"], dados["horario_fechamento"], dados["dias_funcionamento"])
            except ValidationError as erro:
                mostrar_erros_no_form(form, erro)
            else:
                messages.success(request, "Quadra cadastrada com sucesso!")
                return redirect("quadras:cadastro")
    else:
        form = CadastroQuadraForm()

    return render(request, "quadras/cadastro.html", {"form": form})


def editar(request, pk):
    """exibe a quadra preenchida no formulario e salva as alteracoes."""
    quadra = get_object_or_404(Quadra, pk=pk)

    if request.method == "POST":
        form = CadastroQuadraForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            try:
                editar_quadra(quadra, dados["nome"], dados["tipo"], dados["horario_abertura"], dados["horario_fechamento"], dados["dias_funcionamento"])
            except ValidationError as erro:
                mostrar_erros_no_form(form, erro)
            else:
                messages.success(request, "Quadra atualizada com sucesso!")
                return redirect("quadras:editar", pk=quadra.pk)
    else:
        # abre o form ja com os dados atuais da quadra
        form = CadastroQuadraForm(initial={"nome": quadra.nome, "tipo": quadra.tipo, "horario_abertura": quadra.horario_abertura, "horario_fechamento": quadra.horario_fechamento, "dias_funcionamento": quadra.dias_funcionamento})

    return render(request, "quadras/editar.html", {"form": form, "quadra": quadra})


@require_POST
def desativar(request, pk):
    """desativa a quadra e volta pra tela de edicao."""
    quadra = get_object_or_404(Quadra, pk=pk)
    try:
        desativar_quadra(quadra)
    except ValidationError as erro:
        messages.error(request, erro.messages[0])
    else:
        messages.success(request, "Quadra desativada. Ela não aparece mais para reserva.")
    return redirect("quadras:editar", pk=quadra.pk)


@require_POST
def reativar(request, pk):
    """reativa a quadra e volta pra tela de edicao."""
    quadra = get_object_or_404(Quadra, pk=pk)
    try:
        reativar_quadra(quadra)
    except ValidationError as erro:
        messages.error(request, erro.messages[0])
    else:
        messages.success(request, "Quadra reativada. Ela já pode ser reservada de novo.")
    return redirect("quadras:editar", pk=quadra.pk)


def lista(request):
    """mostra as quadras cadastradas e quais delas podem ser reservadas."""
    return render(request, "quadras/lista.html", {"quadras": listar_quadras()})
