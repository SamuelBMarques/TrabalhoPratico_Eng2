"""formularios relacionados a consulta de horarios."""
from django import forms
from django.utils import timezone


class ConsultaHorariosForm(forms.Form):
    """valida a data escolhida na consulta de horarios."""

    data = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        error_messages={"required": "Escolha uma data.", "invalid": "Informe uma data válida."},
    )

    def clean_data(self):
        data = self.cleaned_data["data"]
        if data < timezone.localdate():
            raise forms.ValidationError("Escolha hoje ou uma data futura.")
        return data


class ReservaForm(forms.Form):
    """valida a data e o horario enviados pelo botao de reservar."""

    data = forms.DateField()
    hora_inicio = forms.TimeField()
