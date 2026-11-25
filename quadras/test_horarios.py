"""US11, #25: operações administrativas e integração com a disponibilidade.

Complementa os testes de cadastro, edição, dados inválidos e conflitos de tests.py.
A exclusão adotada pelo projeto é a desativação, preservando os registros.
"""
import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from reservas.models import Reserva
from reservas.services import criar_reserva, listar_horarios_disponiveis

from .models import HorarioFuncionamento
from .services import cadastrar_horario, cadastrar_quadra, desativar_horario, editar_horario


class GerenciamentoHorariosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_user(
            "admin@teste.com", "Administrador", "senha-teste-123", is_staff=True,
        )
        cls.usuario = get_user_model().objects.create_user(
            "aluno@teste.com", "Aluno", "senha-teste-123",
        )
        cls.quadra = cadastrar_quadra(
            "Quadra Central", "Futsal", datetime.time(8), datetime.time(18), ["seg", "qua"],
        )
        cls.horario = cadastrar_horario(cls.quadra, "seg", datetime.time(8), datetime.time(12))

    def setUp(self):
        self.client.force_login(self.admin)

    def url(self, acao):
        return reverse(f"quadras:{acao}_horario", args=[self.horario.pk])

    def test_desativar_e_reativar_pela_interface_preserva_o_registro(self):
        resposta = self.client.post(self.url("desativar"), follow=True)

        self.assertRedirects(resposta, reverse("quadras:horarios", args=[self.quadra.pk]))
        self.assertContains(resposta, "Horário desativado.")
        self.horario.refresh_from_db()
        self.assertFalse(self.horario.ativo)
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)

        resposta = self.client.post(self.url("reativar"), follow=True)

        self.assertContains(resposta, "Horário reativado.")
        self.horario.refresh_from_db()
        self.assertTrue(self.horario.ativo)
        self.assertEqual(self.horario.quadra_id, self.quadra.pk)
        self.assertEqual(self.horario.hora_inicio, datetime.time(8))
        self.assertEqual(self.horario.hora_fim, datetime.time(12))
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)

    def test_repetir_desativacao_ou_reativacao_informa_erro_sem_mudar_estado(self):
        resposta = self.client.post(self.url("reativar"), follow=True)
        self.assertContains(resposta, "O horário já está ativo.")
        self.horario.refresh_from_db()
        self.assertTrue(self.horario.ativo)

        self.client.post(self.url("desativar"))
        resposta = self.client.post(self.url("desativar"), follow=True)
        self.assertContains(resposta, "O horário já está desativado.")
        self.horario.refresh_from_db()
        self.assertFalse(self.horario.ativo)
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)

    def test_get_nao_desativa_nem_reativa(self):
        for acao, ativo in [("desativar", True), ("reativar", False)]:
            with self.subTest(acao=acao):
                self.horario.ativo = ativo
                self.horario.save(update_fields=["ativo"])
                self.assertEqual(self.client.get(self.url(acao)).status_code, 405)
                self.horario.refresh_from_db()
                self.assertEqual(self.horario.ativo, ativo)

    def test_visitante_e_usuario_comum_nao_acessam_telas_nem_alteram_horarios(self):
        telas = [
            reverse("quadras:horarios", args=[self.quadra.pk]),
            reverse("quadras:cadastrar_horario", args=[self.quadra.pk]),
            self.url("editar"),
        ]
        dados = {"dia_semana": "qua", "hora_inicio": "10:00", "hora_fim": "14:00", "ativo": "on"}
        for usuario, status in [(None, 302), (self.usuario, 403)]:
            self.client.logout()
            if usuario:
                self.client.force_login(usuario)
            for url in telas:
                with self.subTest(usuario=usuario, tela=url):
                    self.assertEqual(self.client.get(url).status_code, status)
            for ativo in [True, False]:
                self.horario.ativo = ativo
                self.horario.save(update_fields=["ativo"])
                for url in telas[1:] + [self.url("desativar"), self.url("reativar")]:
                    with self.subTest(usuario=usuario, operacao=url, ativo=ativo):
                        resposta = self.client.post(url, dados)
                        self.assertEqual(resposta.status_code, status)
                        self.horario.refresh_from_db()
                        self.assertEqual(self.horario.ativo, ativo)
                        self.assertEqual(self.horario.dia_semana, "seg")
                        self.assertEqual(self.horario.hora_inicio, datetime.time(8))
                        self.assertEqual(HorarioFuncionamento.objects.count(), 1)

    def test_operacoes_sem_csrf_sao_recusadas(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.admin)
        urls = [reverse("quadras:cadastrar_horario", args=[self.quadra.pk]), self.url("editar")]
        for ativo in [True, False]:
            self.horario.ativo = ativo
            self.horario.save(update_fields=["ativo"])
            for url in urls + [self.url("desativar"), self.url("reativar")]:
                with self.subTest(url=url, ativo=ativo):
                    self.assertEqual(cliente.post(url, {}).status_code, 403)
                    self.horario.refresh_from_db()
                    self.assertEqual(self.horario.ativo, ativo)
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)

    def test_recursos_inexistentes_retornam_404(self):
        for nome in ["horarios", "cadastrar_horario", "editar_horario", "desativar_horario", "reativar_horario"]:
            with self.subTest(nome=nome):
                resposta = self.client.post(reverse(f"quadras:{nome}", args=[999]), {})
                self.assertEqual(resposta.status_code, 404)

    def test_listagem_nao_mistura_horarios_de_outras_quadras(self):
        outra = cadastrar_quadra("Outra", "Vôlei", datetime.time(8), datetime.time(18), ["seg"])
        horario = cadastrar_horario(outra, "seg", datetime.time(15), datetime.time(17))

        resposta = self.client.get(reverse("quadras:horarios", args=[self.quadra.pk]))

        self.assertEqual([h.pk for h in resposta.context["horarios"]], [self.horario.pk])
        self.assertNotContains(resposta, reverse("quadras:editar_horario", args=[horario.pk]))


class DisponibilidadeComHorariosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user("aluno@teste.com", "Aluno", "senha-teste-123")
        cls.quadra = cadastrar_quadra("Quadra", "Futsal", datetime.time(8), datetime.time(12), ["seg", "qua"])

    def setUp(self):
        # Datas fixas: a passagem do tempo não muda o resultado destes testes.
        self.data = datetime.date(2030, 1, 7)  # segunda-feira
        relogio = patch("reservas.services.timezone.localtime", return_value=datetime.datetime(2030, 1, 1, 7))
        relogio.start()
        self.addCleanup(relogio.stop)

    def inicios(self, data=None):
        return [h.inicio.hour for h in listar_horarios_disponiveis(self.quadra, data or self.data)]

    def test_cadastro_substitui_funcionamento_geral_apenas_no_dia_escolhido(self):
        self.assertEqual(self.inicios(), [8, 9, 10, 11])
        cadastrar_horario(self.quadra, "seg", datetime.time(14), datetime.time(16))

        self.assertEqual(self.inicios(), [14, 15])
        self.assertEqual(self.inicios(datetime.date(2030, 1, 9)), [8, 9, 10, 11])

    def test_multiplos_periodos_respeitam_intervalo_e_ignoram_inativos(self):
        cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(10))
        cadastrar_horario(self.quadra, "seg", datetime.time(14), datetime.time(16))
        cadastrar_horario(self.quadra, "seg", datetime.time(10), datetime.time(12), False)

        self.assertEqual(self.inicios(), [8, 9, 14, 15])

    def test_edicao_atualiza_disponibilidade_sem_manter_periodo_antigo(self):
        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(10))
        editar_horario(horario, "seg", datetime.time(14), datetime.time(16))

        self.assertEqual(self.inicios(), [14, 15])

    def test_desativar_ultimo_periodo_fecha_dia_e_impede_nova_reserva(self):
        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(10))
        desativar_horario(horario)

        self.assertEqual(self.inicios(), [])
        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, self.data, datetime.time(8))
        self.assertFalse(Reserva.objects.exists())

    def test_reativar_reabre_dia_para_reservas(self):
        from .services import reativar_horario

        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(10), False)
        self.assertEqual(self.inicios(), [])
        reativar_horario(horario)

        reserva = criar_reserva(self.usuario, self.quadra, self.data, datetime.time(8))
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.CONFIRMADA)
        self.assertEqual(self.inicios(), [9])

    def test_desativar_preserva_reserva_existente(self):
        horario = cadastrar_horario(self.quadra, "seg", datetime.time(8), datetime.time(10))
        reserva = criar_reserva(self.usuario, self.quadra, self.data, datetime.time(8))

        desativar_horario(horario)

        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.CONFIRMADA)
        self.assertEqual(reserva.usuario_id, self.usuario.pk)
        self.assertEqual(reserva.quadra_id, self.quadra.pk)
        self.assertEqual((reserva.hora_inicio, reserva.hora_fim), (datetime.time(8), datetime.time(9)))
        self.assertTrue(HorarioFuncionamento.objects.filter(pk=horario.pk, ativo=False).exists())
        self.assertEqual(self.inicios(), [])
