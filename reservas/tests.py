import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from quadras.services import cadastrar_quadra, desativar_quadra

from .models import Bloqueio, Reserva
from .services import Horario, criar_reserva, horario_esta_disponivel, listar_horarios_disponiveis

TODOS_OS_DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
SEGUNDA = datetime.date(2030, 1, 7)
TERCA = datetime.date(2030, 1, 8)


def hora(texto):
    return datetime.time.fromisoformat(texto)


def criar_quadra(abertura="08:00", fechamento="11:00", dias=None, nome="Quadra 1"):
    return cadastrar_quadra(nome, "Futsal", hora(abertura), hora(fechamento), dias or TODOS_OS_DIAS)


def inserir_reserva(quadra, data, inicio, fim, status=Reserva.CONFIRMADA):
    usuario, _ = get_user_model().objects.get_or_create(email="aluno@teste.com", defaults={"nome": "Aluno"})
    return Reserva.objects.create(usuario=usuario, quadra=quadra, data=data, hora_inicio=hora(inicio), hora_fim=hora(fim), status=status)


def inicios(horarios):
    return [horario.inicio.strftime("%H:%M") for horario in horarios]


class HorariosDisponiveisTests(TestCase):
    """H04: regras de disponibilidade."""

    # antes de todas as datas usadas nos testes
    agora = datetime.datetime(2030, 1, 1, 12, 0)

    def listar(self, quadra, data=SEGUNDA, agora=None):
        return listar_horarios_disponiveis(quadra, data, agora or self.agora)

    def test_divide_o_funcionamento_em_horarios_de_uma_hora(self):
        self.assertEqual(
            self.listar(criar_quadra()),
            [Horario(hora("08:00"), hora("09:00")), Horario(hora("09:00"), hora("10:00")), Horario(hora("10:00"), hora("11:00"))],
        )

    def test_sobra_menor_que_uma_hora_nao_vira_horario(self):
        self.assertEqual(inicios(self.listar(criar_quadra("08:00", "09:30"))), ["08:00"])

    def test_funcionamento_menor_que_uma_hora_nao_tem_horario(self):
        self.assertEqual(self.listar(criar_quadra("08:00", "08:30")), [])

    def test_dia_em_que_a_quadra_nao_abre_nao_tem_horario(self):
        quadra = criar_quadra(dias=["seg"])

        self.assertEqual(len(self.listar(quadra, SEGUNDA)), 3)
        self.assertEqual(self.listar(quadra, TERCA), [])

    def test_quadra_desativada_nao_tem_horario(self):
        quadra = desativar_quadra(criar_quadra())

        self.assertEqual(self.listar(quadra), [])

    def test_reserva_confirmada_ocupa_o_horario(self):
        quadra = criar_quadra()
        inserir_reserva(quadra, SEGUNDA, "09:00", "10:00")

        self.assertEqual(inicios(self.listar(quadra)), ["08:00", "10:00"])

    def test_reserva_cancelada_libera_o_horario(self):
        quadra = criar_quadra()
        inserir_reserva(quadra, SEGUNDA, "09:00", "10:00", Reserva.CANCELADA)

        self.assertEqual(len(self.listar(quadra)), 3)

    def test_bloqueio_ocupa_o_horario(self):
        quadra = criar_quadra()
        Bloqueio.objects.create(quadra=quadra, data=SEGUNDA, hora_inicio=hora("08:00"), hora_fim=hora("09:00"))

        self.assertEqual(inicios(self.listar(quadra)), ["09:00", "10:00"])

    def test_periodo_parcial_ocupa_todo_horario_que_ele_toca(self):
        quadra = criar_quadra()
        Bloqueio.objects.create(quadra=quadra, data=SEGUNDA, hora_inicio=hora("08:30"), hora_fim=hora("09:30"))

        self.assertEqual(inicios(self.listar(quadra)), ["10:00"])

    def test_periodo_encostado_nao_ocupa_o_horario_vizinho(self):
        quadra = criar_quadra()
        Bloqueio.objects.create(quadra=quadra, data=SEGUNDA, hora_inicio=hora("09:00"), hora_fim=hora("10:00"))

        self.assertEqual(inicios(self.listar(quadra)), ["08:00", "10:00"])

    def test_ocupacao_de_outra_quadra_ou_outra_data_nao_interfere(self):
        quadra = criar_quadra()
        outra = criar_quadra(nome="Quadra 2")
        inserir_reserva(outra, SEGUNDA, "08:00", "09:00")
        inserir_reserva(quadra, TERCA, "08:00", "09:00")

        self.assertEqual(len(self.listar(quadra, SEGUNDA)), 3)

    def test_hoje_nao_mostra_horario_que_ja_comecou(self):
        agora = datetime.datetime.combine(SEGUNDA, hora("09:30"))

        self.assertEqual(inicios(self.listar(criar_quadra(), SEGUNDA, agora)), ["10:00"])

    def test_data_passada_nao_tem_horario(self):
        agora = datetime.datetime.combine(TERCA, hora("07:00"))

        self.assertEqual(self.listar(criar_quadra(), SEGUNDA, agora), [])

    def test_revalidacao_recusa_horario_que_foi_ocupado(self):
        quadra = criar_quadra()

        self.assertTrue(horario_esta_disponivel(quadra, SEGUNDA, hora("09:00"), hora("10:00")))
        inserir_reserva(quadra, SEGUNDA, "09:00", "10:00")
        self.assertFalse(horario_esta_disponivel(quadra, SEGUNDA, hora("09:00"), hora("10:00")))

    def test_revalidacao_recusa_horario_fora_da_grade(self):
        self.assertFalse(horario_esta_disponivel(criar_quadra(), SEGUNDA, hora("08:30"), hora("09:30")))


class TelaHorariosTests(TestCase):
    """H04: tela de consulta."""

    def abrir(self, quadra, **params):
        return self.client.get(reverse("reservas:horarios", args=[quadra.pk]), params)

    def test_consulta_mostra_horarios_da_data_escolhida(self):
        resposta = self.abrir(criar_quadra(), data="2030-01-07")

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "07/01/2030")
        self.assertContains(resposta, "08:00 às 09:00")
        self.assertContains(resposta, "10:00 às 11:00")

    def test_sem_data_consulta_o_dia_de_hoje(self):
        resposta = self.abrir(criar_quadra())

        self.assertContains(resposta, timezone.localdate().strftime("%d/%m/%Y"))

    def test_horario_reservado_nao_aparece_e_nao_revela_quem_reservou(self):
        quadra = criar_quadra()
        inserir_reserva(quadra, SEGUNDA, "09:00", "10:00")

        resposta = self.abrir(quadra, data="2030-01-07")

        self.assertNotContains(resposta, "09:00 às 10:00")
        self.assertNotContains(resposta, "aluno@teste.com")

    def test_sem_horarios_exibe_indicacao(self):
        resposta = self.abrir(criar_quadra(dias=["ter"]), data="2030-01-07")

        self.assertContains(resposta, "Nenhum horário disponível")

    def test_data_passada_exibe_erro(self):
        resposta = self.abrir(criar_quadra(), data="2020-01-06")

        self.assertContains(resposta, "Escolha hoje ou uma data futura.")
        self.assertNotContains(resposta, "Horários livres em")

    def test_data_invalida_exibe_erro(self):
        resposta = self.abrir(criar_quadra(), data="abc")

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Informe uma data válida.")

    def test_quadra_desativada_avisa_e_nao_oferece_consulta(self):
        resposta = self.abrir(desativar_quadra(criar_quadra()), data="2030-01-07")

        self.assertContains(resposta, "Quadra indisponível")
        self.assertNotContains(resposta, "08:00 às 09:00")

    def test_quadra_inexistente_retorna_404(self):
        resposta = self.client.get(reverse("reservas:horarios", args=[999]))

        self.assertEqual(resposta.status_code, 404)

    def test_lista_de_quadras_liga_para_a_consulta_so_nas_ativas(self):
        ativa = criar_quadra(nome="Ativa")
        desativada = desativar_quadra(criar_quadra(nome="Desativada"))

        resposta = self.client.get(reverse("quadras:lista"))

        self.assertContains(resposta, reverse("reservas:horarios", args=[ativa.pk]))
        self.assertNotContains(resposta, reverse("reservas:horarios", args=[desativada.pk]))


class CriarReservaTests(TestCase):
    """H05: regras da criacao da reserva."""

    def setUp(self):
        self.usuario = get_user_model().objects.create_user("aluno@teste.com", "Aluno", "senha-forte-123")
        self.outro = get_user_model().objects.create_user("outro@teste.com", "Outro", "senha-forte-123")
        self.quadra = criar_quadra()

    def test_registra_usuario_quadra_data_e_horario(self):
        reserva = criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))

        reserva.refresh_from_db()
        self.assertEqual(reserva.usuario, self.usuario)
        self.assertEqual(reserva.quadra, self.quadra)
        self.assertEqual(reserva.data, SEGUNDA)
        self.assertEqual((reserva.hora_inicio, reserva.hora_fim), (hora("09:00"), hora("10:00")))
        self.assertEqual(reserva.status, Reserva.CONFIRMADA)

    def test_horario_reservado_some_da_consulta(self):
        criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))

        self.assertEqual(inicios(listar_horarios_disponiveis(self.quadra, SEGUNDA)), ["08:00", "10:00"])

    def test_recusa_horario_ja_reservado_por_outra_pessoa(self):
        criar_reserva(self.outro, self.quadra, SEGUNDA, hora("09:00"))

        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))
        self.assertEqual(Reserva.objects.count(), 1)

    def test_aceita_horario_de_reserva_cancelada(self):
        cancelada = criar_reserva(self.outro, self.quadra, SEGUNDA, hora("09:00"))
        cancelada.status = Reserva.CANCELADA
        cancelada.save()

        reserva = criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))

        self.assertEqual(reserva.usuario, self.usuario)

    def test_recusa_periodo_bloqueado(self):
        Bloqueio.objects.create(quadra=self.quadra, data=SEGUNDA, hora_inicio=hora("09:00"), hora_fim=hora("10:00"))

        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))

    def test_recusa_fora_do_horario_de_funcionamento(self):
        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("11:00"))

    def test_recusa_dia_em_que_a_quadra_nao_abre(self):
        quadra = criar_quadra(dias=["ter"], nome="So terca")

        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, quadra, SEGUNDA, hora("09:00"))

    def test_recusa_inicio_fora_da_grade(self):
        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:30"))

    def test_recusa_quadra_desativada(self):
        desativar_quadra(self.quadra)

        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))

    def test_recusa_data_passada(self):
        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, self.quadra, datetime.date(2020, 1, 6), hora("09:00"))

    def test_horario_no_fim_do_dia_nao_quebra(self):
        quadra = criar_quadra("22:00", "23:59", nome="Noturna")

        with self.assertRaises(ValidationError):
            criar_reserva(self.usuario, quadra, SEGUNDA, hora("23:30"))

    def test_disputa_pelo_mesmo_horario_vira_recusa_amigavel(self):
        # simula as duas pessoas passando juntas pela verificacao: quem chega depois cai na regra do banco
        criar_reserva(self.outro, self.quadra, SEGUNDA, hora("09:00"))

        with mock.patch("reservas.services.horario_esta_disponivel", return_value=True):
            with transaction.atomic(), self.assertRaises(ValidationError):
                criar_reserva(self.usuario, self.quadra, SEGUNDA, hora("09:00"))
        self.assertEqual(Reserva.objects.count(), 1)

    def test_banco_impede_duas_confirmadas_no_mesmo_horario(self):
        criar_reserva(self.outro, self.quadra, SEGUNDA, hora("09:00"))

        with self.assertRaises(IntegrityError), transaction.atomic():
            Reserva.objects.create(usuario=self.usuario, quadra=self.quadra, data=SEGUNDA, hora_inicio=hora("09:00"), hora_fim=hora("10:00"))


class TelaReservaTests(TestCase):
    """H05: fluxo de reservar pela tela."""

    def setUp(self):
        self.usuario = get_user_model().objects.create_user("aluno@teste.com", "Aluno Teste", "senha-forte-123")
        self.quadra = criar_quadra()
        self.url_horarios = reverse("reservas:horarios", args=[self.quadra.pk])
        self.url_reservar = reverse("reservas:reservar", args=[self.quadra.pk])
        self.dados = {"data": "2030-01-07", "hora_inicio": "09:00"}

    def test_visitante_ve_horarios_e_convite_para_entrar_sem_botao(self):
        resposta = self.client.get(self.url_horarios, {"data": "2030-01-07"})

        self.assertContains(resposta, "08:00 às 09:00")
        self.assertContains(resposta, "Entre na sua conta")
        self.assertContains(resposta, "next=%2Freservas%2Fquadras%2F")
        self.assertNotContains(resposta, "Reservar</button>")

    def test_usuario_logado_ve_botao_de_reservar(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(self.url_horarios, {"data": "2030-01-07"})

        self.assertContains(resposta, "Reservar</button>", count=3)
        self.assertContains(resposta, "Olá, Aluno")

    def test_visitante_nao_consegue_reservar(self):
        resposta = self.client.post(self.url_reservar, self.dados)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("usuarios:login"), resposta["Location"])
        self.assertFalse(Reserva.objects.exists())

    def test_reserva_fica_com_o_usuario_logado_e_mostra_confirmacao(self):
        outro = get_user_model().objects.create_user("outro@teste.com", "Outro", "senha-forte-123")
        self.client.force_login(self.usuario)

        resposta = self.client.post(self.url_reservar, {**self.dados, "usuario": outro.pk}, follow=True)

        self.assertEqual(Reserva.objects.get().usuario, self.usuario)
        self.assertRedirects(resposta, f"{self.url_horarios}?data=2030-01-07")
        self.assertContains(resposta, "Reserva confirmada: Quadra 1, 07/01/2030, das 09:00 às 10:00.")
        self.assertNotContains(resposta, "<span>09:00 às 10:00</span>")

    def test_horario_ocupado_informa_o_usuario_e_nao_cria_reserva(self):
        outro = get_user_model().objects.create_user("outro@teste.com", "Outro", "senha-forte-123")
        criar_reserva(outro, self.quadra, SEGUNDA, hora("09:00"))
        self.client.force_login(self.usuario)

        resposta = self.client.post(self.url_reservar, self.dados, follow=True)

        self.assertContains(resposta, "Esse horário não está mais disponível.")
        self.assertEqual(Reserva.objects.count(), 1)

    def test_dados_invalidos_informam_o_usuario(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(self.url_reservar, {"data": "abc", "hora_inicio": "xyz"}, follow=True)

        self.assertContains(resposta, "Não foi possível reservar.")
        self.assertFalse(Reserva.objects.exists())

    def test_get_em_reservar_volta_para_os_horarios_sem_criar_nada(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(self.url_reservar)

        self.assertRedirects(resposta, self.url_horarios)
        self.assertFalse(Reserva.objects.exists())

    def test_post_sem_token_csrf_e_recusado(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)

        resposta = cliente.post(self.url_reservar, self.dados)

        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(Reserva.objects.exists())

    def test_quadra_inexistente_retorna_404(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse("reservas:reservar", args=[999]), self.dados)

        self.assertEqual(resposta.status_code, 404)
