import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import HorarioFuncionamento
from .services import cadastrar_horario, cadastrar_quadra, desativar_quadra, editar_horario, editar_quadra, listar_quadras


def criar_quadra(nome="Quadra 1", tipo="Futsal", dias=None):
    return cadastrar_quadra(nome, tipo, datetime.time(8, 0), datetime.time(22, 0), dias or ["seg", "qua"])


class ListagemQuadrasTests(TestCase):
    """H03: visualizar quadras."""

    def abrir_lista(self):
        return self.client.get(reverse("quadras:lista"))

    def test_mostra_dados_que_identificam_a_quadra(self):
        criar_quadra("Ginásio Central", "Poliesportiva")

        resposta = self.abrir_lista()

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ginásio Central")
        self.assertContains(resposta, "Poliesportiva")
        self.assertContains(resposta, "Disponível para reserva")

    def test_mostra_horario_e_dias_de_funcionamento(self):
        criar_quadra(dias=["qua", "seg"])

        resposta = self.abrir_lista()

        self.assertContains(resposta, "08:00 às 22:00")
        self.assertContains(resposta, "Segunda, Quarta")

    def test_quadra_desativada_aparece_como_indisponivel(self):
        desativar_quadra(criar_quadra("Quadra Velha"))

        resposta = self.abrir_lista()

        self.assertContains(resposta, "Quadra Velha")
        self.assertContains(resposta, "Indisponível para reserva")
        self.assertNotContains(resposta, "Disponível para reserva")

    def test_lista_reflete_edicao_da_quadra(self):
        quadra = criar_quadra("Nome Antigo")
        editar_quadra(quadra, "Nome Novo", "Vôlei", quadra.horario_abertura, quadra.horario_fechamento, ["sex"])

        resposta = self.abrir_lista()

        self.assertContains(resposta, "Nome Novo")
        self.assertNotContains(resposta, "Nome Antigo")

    def test_lista_vazia_informa_que_nao_ha_quadras(self):
        self.assertContains(self.abrir_lista(), "Nenhuma quadra cadastrada")

    def test_conteudo_da_quadra_e_escapado(self):
        criar_quadra("<script>alert(1)</script>")

        resposta = self.abrir_lista()

        self.assertNotContains(resposta, "<script>alert(1)</script>")
        self.assertContains(resposta, "&lt;script&gt;")

    def test_ativas_vem_primeiro_e_depois_ordem_alfabetica(self):
        desativar_quadra(criar_quadra("Arena"))
        criar_quadra("zebra")
        criar_quadra("Bosque")

        self.assertEqual([quadra.nome for quadra in listar_quadras()], ["Bosque", "zebra", "Arena"])


class HorariosFuncionamentoTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user("admin@teste.com", "Administrador", "senha-forte-123", is_staff=True)
        self.usuario = get_user_model().objects.create_user("aluno@teste.com", "Aluno", "senha-forte-123")
        self.quadra = criar_quadra("Ginásio Principal")
        self.dados = {
            "dia_semana": "seg",
            "hora_inicio": "08:00",
            "hora_fim": "12:00",
            "ativo": "on",
        }

    def test_cadastrar_horario_persiste_dados_da_quadra(self):
        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(12))

        self.assertEqual(horario.quadra, self.quadra)
        self.assertEqual(horario.dia_semana, "seg")
        self.assertTrue(horario.ativo)

    def test_editar_horario_atualiza_dia_e_intervalo(self):
        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(12))

        editar_horario(horario, "qua", datetime.time(10), datetime.time(18), False)

        horario.refresh_from_db()
        self.assertEqual((horario.dia_semana, horario.hora_inicio, horario.hora_fim, horario.ativo), ("qua", datetime.time(10), datetime.time(18), False))

    def test_formulario_recusa_fechamento_antes_da_abertura(self):
        self.client.force_login(self.admin)
        resposta = self.client.post(reverse("quadras:cadastrar_horario", args=[self.quadra.pk]), {**self.dados, "hora_inicio": "13:00", "hora_fim": "12:00"})

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "O horário de fechamento deve ser depois da abertura.")
        self.assertFalse(HorarioFuncionamento.objects.exists())

    def test_admin_cadastra_e_edita_horario_pela_interface(self):
        self.client.force_login(self.admin)

        resposta = self.client.post(reverse("quadras:cadastrar_horario", args=[self.quadra.pk]), self.dados, follow=True)

        self.assertRedirects(resposta, reverse("quadras:horarios", args=[self.quadra.pk]))
        horario = HorarioFuncionamento.objects.get()
        self.assertContains(resposta, "Segunda: 08:00 às 12:00")

        resposta = self.client.post(reverse("quadras:editar_horario", args=[horario.pk]), {**self.dados, "dia_semana": "qua", "hora_inicio": "10:00", "hora_fim": "18:00"}, follow=True)

        horario.refresh_from_db()
        self.assertRedirects(resposta, reverse("quadras:horarios", args=[self.quadra.pk]))
        self.assertEqual((horario.dia_semana, horario.hora_inicio, horario.hora_fim), ("qua", datetime.time(10), datetime.time(18)))

    def test_usuario_comum_nao_acessa_gerenciamento_de_horarios(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse("quadras:horarios", args=[self.quadra.pk]))

        self.assertEqual(resposta.status_code, 403)
