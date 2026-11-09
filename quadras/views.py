"""views relacionadas ao cadastro, edicao e desativacao de quadras."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroQuadraForm, HorarioFuncionamentoForm
from .models import HorarioFuncionamento, Quadra
from .services import cadastrar_horario, cadastrar_quadra, desativar_quadra, editar_horario, editar_quadra, reativar_quadra
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


def exigir_administrador(request):
    if not request.user.is_authenticated:
        return redirect("usuarios:login")
    if not request.user.is_staff:
        raise PermissionDenied
    return None


@login_required
def horarios(request, quadra_id):
    bloqueio = exigir_administrador(request)
    if bloqueio:
        return bloqueio
    quadra = get_object_or_404(Quadra, pk=quadra_id)
    horarios = quadra.horarios_funcionamento.all()
    return render(request, "quadras/horarios.html", {"quadra": quadra, "horarios": horarios})


@login_required
def cadastrar_horario_view(request, quadra_id):
    bloqueio = exigir_administrador(request)
    if bloqueio:
        return bloqueio
    quadra = get_object_or_404(Quadra, pk=quadra_id)
    if request.method == "POST":
        form = HorarioFuncionamentoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cadastrar_horario(quadra, dados["dia_semana"], dados["hora_inicio"], dados["hora_fim"], dados["ativo"])
            messages.success(request, "Horário cadastrado com sucesso!")
            return redirect("quadras:horarios", quadra_id=quadra.pk)
    else:
        form = HorarioFuncionamentoForm()
    return render(request, "quadras/horario_form.html", {"form": form, "quadra": quadra, "titulo": "Cadastrar horário"})


@login_required
def editar_horario_view(request, pk):
    bloqueio = exigir_administrador(request)
    if bloqueio:
        return bloqueio
    horario = get_object_or_404(HorarioFuncionamento, pk=pk)
    if request.method == "POST":
        form = HorarioFuncionamentoForm(request.POST, instance=horario)
        if form.is_valid():
            dados = form.cleaned_data
            editar_horario(horario, dados["dia_semana"], dados["hora_inicio"], dados["hora_fim"], dados["ativo"])
            messages.success(request, "Horário atualizado com sucesso!")
            return redirect("quadras:horarios", quadra_id=horario.quadra_id)
    else:
        form = HorarioFuncionamentoForm(instance=horario)
    return render(request, "quadras/horario_form.html", {"form": form, "quadra": horario.quadra, "horario": horario, "titulo": "Editar horário"})
