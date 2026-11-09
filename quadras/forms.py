"""formularios relacionados ao cadastro de quadras."""
import datetime

from django import forms

from .models import HorarioFuncionamento, Quadra


class CadastroQuadraForm(forms.Form):
    """valida os dados enviados pela tela de cadastro de quadra."""

    nome = forms.CharField( label="Nome da quadra", max_length=150, widget=forms.TextInput(attrs={"placeholder": "Ex.: Quadra 1"}),)

    tipo = forms.CharField( label="Tipo", max_length=150, widget=forms.TextInput(attrs={"placeholder": "Ex.: futsal, vôlei", "list": "sugestoes-tipo"}),)

    horario_abertura = forms.TimeField( label="Abre às", initial=datetime.time(8, 0), widget=forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),)

    horario_fechamento = forms.TimeField( label="Fecha às", initial=datetime.time(22, 0), widget=forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),)

    dias_funcionamento = forms.MultipleChoiceField( label="Dias de funcionamento", choices=Quadra.DIAS_SEMANA, widget=forms.CheckboxSelectMultiple, error_messages={"required": "Escolha pelo menos um dia."},)

    def clean(self):
        dados = super().clean()
        abertura = dados.get("horario_abertura")
        fechamento = dados.get("horario_fechamento")
        if abertura and fechamento and fechamento <= abertura:
            self.add_error("horario_fechamento", "O horário de fechamento deve ser depois da abertura.")
        return dados


class HorarioFuncionamentoForm(forms.ModelForm):
    class Meta:
        model = HorarioFuncionamento
        fields = ["dia_semana", "hora_inicio", "hora_fim", "ativo"]
        widgets = {
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "hora_fim": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }

    def clean(self):
        dados = super().clean()
        inicio = dados.get("hora_inicio")
        fim = dados.get("hora_fim")
        if inicio and fim and fim <= inicio:
            self.add_error("hora_fim", "O horário de fechamento deve ser depois da abertura.")
        return dados
