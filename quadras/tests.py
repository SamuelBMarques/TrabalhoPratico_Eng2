import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import HorarioFuncionamento, Quadra
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

class InterfaceGerenciamentoQuadrasTests(TestCase):
    """US10, #34: navegação administrativa e proteção das operações."""

    def setUp(self):
        self.quadra = criar_quadra()
        self.admin = get_user_model().objects.create_user(
            email="gestor@teste.com", nome="Gestor", password="senha-teste-123", is_staff=True,
        )
        self.usuario = get_user_model().objects.create_user(
            email="comum@teste.com", nome="Aluno", password="senha-teste-123",
        )

    def test_administrador_encontra_cadastro_e_edicao_inclusive_de_desativadas(self):
        desativar_quadra(self.quadra)
        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("quadras:gerenciar"))

        self.assertContains(resposta, "Gerenciar quadras")
        self.assertContains(resposta, reverse("quadras:cadastro"))
        self.assertContains(resposta, reverse("quadras:editar", args=[self.quadra.pk]))
        self.assertContains(resposta, self.quadra.nome)
        self.assertContains(resposta, "Indisponível para reserva")

    def test_gerenciamento_vazio_mantem_acesso_ao_cadastro(self):
        self.quadra.delete()
        self.client.force_login(self.admin)
        resposta = self.client.get(reverse("quadras:gerenciar"))
        self.assertContains(resposta, "Nenhuma quadra cadastrada")
        self.assertContains(resposta, reverse("quadras:cadastro"))

    def test_telas_permitem_voltar_ao_gerenciamento(self):
        self.client.force_login(self.admin)
        for url in [reverse("quadras:cadastro"), reverse("quadras:editar", args=[self.quadra.pk])]:
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), reverse("quadras:gerenciar"))

    def test_catalogo_so_exibe_acesso_administrativo_para_staff(self):
        url = reverse("quadras:gerenciar")
        self.assertNotContains(self.client.get(reverse("quadras:lista")), url)
        self.client.force_login(self.usuario)
        self.assertNotContains(self.client.get(reverse("quadras:lista")), url)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("quadras:lista")), url)

    def test_visitante_e_usuario_comum_nao_acessam_operacoes_administrativas(self):
        urls = [
            reverse("quadras:gerenciar"), reverse("quadras:cadastro"),
            reverse("quadras:editar", args=[self.quadra.pk]),
            reverse("quadras:desativar", args=[self.quadra.pk]),
            reverse("quadras:reativar", args=[self.quadra.pk]),
        ]
        for usuario, esperado in [(None, 302), (self.usuario, 403)]:
            if usuario:
                self.client.force_login(usuario)
            for url in urls:
                with self.subTest(usuario=usuario, url=url):
                    resposta = self.client.post(url, {})
                    self.assertEqual(resposta.status_code, esperado)
            self.quadra.refresh_from_db()
            self.assertTrue(self.quadra.ativa)
            self.assertEqual(Quadra.objects.count(), 1)


class GerenciamentoQuadrasTests(TestCase):
    """US10, subissue #29: cadastro, edição e desativação pela interface."""

    def setUp(self):
        administrador = get_user_model().objects.create_superuser(
            email="admin@teste.com", nome="Administrador", password="senha-teste-123"
        )
        self.client.force_login(administrador)
        self.dados = {
            "nome": "Quadra Central", "tipo": "Futsal",
            "horario_abertura": "08:00", "horario_fechamento": "22:00",
            "dias_funcionamento": ["seg", "qua"],
        }

    def test_cadastro_persiste_dados_e_informa_sucesso(self):
        resposta = self.client.post(reverse("quadras:cadastro"), self.dados, follow=True)

        quadra = Quadra.objects.get()
        self.assertEqual(quadra.nome, "Quadra Central")
        self.assertEqual(quadra.tipo, "Futsal")
        self.assertEqual(quadra.horario_abertura, datetime.time(8))
        self.assertEqual(quadra.horario_fechamento, datetime.time(22))
        self.assertEqual(quadra.dias_funcionamento, ["seg", "qua"])
        self.assertTrue(quadra.ativa)
        self.assertContains(resposta, "Quadra cadastrada com sucesso!")

    def test_cadastro_invalido_nao_persiste(self):
        casos = [
            {"nome": " "}, {"tipo": ""}, {"dias_funcionamento": []},
            {"dias_funcionamento": ["invalido"]},
            {"horario_abertura": "invalido"},
            {"horario_fechamento": "08:00"},
            {"horario_fechamento": "07:00"},
        ]
        for alteracao in casos:
            with self.subTest(alteracao=alteracao):
                resposta = self.client.post(reverse("quadras:cadastro"), {**self.dados, **alteracao})
                self.assertEqual(resposta.status_code, 200)
                self.assertTrue(resposta.context["form"].errors)
                self.assertFalse(Quadra.objects.exists())

    def test_cadastro_recusa_nome_repetido_sem_distinguir_maiusculas(self):
        criar_quadra("Quadra Central")
        resposta = self.client.post(reverse("quadras:cadastro"), {**self.dados, "nome": " quadra central "})

        self.assertContains(resposta, "Já existe uma quadra com este nome.")
        self.assertEqual(Quadra.objects.count(), 1)

    def test_edicao_atualiza_a_mesma_quadra(self):
        quadra = criar_quadra()
        resposta = self.client.post(reverse("quadras:editar", args=[quadra.pk]), self.dados, follow=True)

        quadra.refresh_from_db()
        self.assertEqual(quadra.nome, "Quadra Central")
        self.assertEqual(Quadra.objects.count(), 1)
        self.assertContains(resposta, "Quadra atualizada com sucesso!")

    def test_edicao_invalida_preserva_dados_originais(self):
        quadra = criar_quadra("Original")
        resposta = self.client.post(reverse("quadras:editar", args=[quadra.pk]), {
            **self.dados, "horario_fechamento": "07:00",
        })

        quadra.refresh_from_db()
        self.assertTrue(resposta.context["form"].errors)
        self.assertEqual(quadra.nome, "Original")
        self.assertEqual(quadra.horario_fechamento, datetime.time(22))

    def test_desativacao_preserva_quadra_e_reservas(self):
        from reservas.models import Reserva
        usuario = get_user_model().objects.create_user(email="aluno@teste.com", nome="Aluno", password="senha-teste-123")
        quadra = criar_quadra()
        reserva = Reserva.objects.create(
            usuario=usuario, quadra=quadra, data=datetime.date(2030, 1, 7),
            hora_inicio=datetime.time(8), hora_fim=datetime.time(9),
        )

        resposta = self.client.post(reverse("quadras:desativar", args=[quadra.pk]), follow=True)

        quadra.refresh_from_db()
        reserva.refresh_from_db()
        self.assertFalse(quadra.ativa)
        self.assertEqual(reserva.quadra_id, quadra.pk)
        self.assertEqual(reserva.status, Reserva.CONFIRMADA)
        self.assertContains(resposta, "Quadra desativada.")

    def test_get_nao_desativa_quadra(self):
        quadra = criar_quadra()
        resposta = self.client.get(reverse("quadras:desativar", args=[quadra.pk]))

        quadra.refresh_from_db()
        self.assertEqual(resposta.status_code, 405)
        self.assertTrue(quadra.ativa)

    def test_edicao_de_quadra_inexistente_retorna_404(self):
        resposta = self.client.post(reverse("quadras:editar", args=[999]), self.dados)
        self.assertEqual(resposta.status_code, 404)
