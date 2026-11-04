import datetime

from django.test import TestCase
from django.urls import reverse

from .services import cadastrar_quadra, desativar_quadra, editar_quadra, listar_quadras


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
