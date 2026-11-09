from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("quadras", "0002_quadra_dias_funcionamento_quadra_horario_abertura_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HorarioFuncionamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dia_semana", models.CharField(choices=[("seg", "Segunda"), ("ter", "Terça"), ("qua", "Quarta"), ("qui", "Quinta"), ("sex", "Sexta"), ("sab", "Sábado"), ("dom", "Domingo")], max_length=3)),
                ("hora_inicio", models.TimeField()),
                ("hora_fim", models.TimeField()),
                ("ativo", models.BooleanField(default=True)),
                ("quadra", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="horarios_funcionamento", to="quadras.quadra")),
            ],
            options={
                "ordering": ["dia_semana", "hora_inicio"],
                "constraints": [models.CheckConstraint(condition=models.Q(("hora_fim__gt", models.F("hora_inicio"))), name="horario_fim_depois_do_inicio")],
            },
        ),
    ]