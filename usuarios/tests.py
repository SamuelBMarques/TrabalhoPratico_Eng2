from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):
    """login e logout usados pela reserva."""

    def setUp(self):
        self.usuario = get_user_model().objects.create_user("aluno@teste.com", "Aluno Teste", "senha-forte-123")

    def entrar(self, email="aluno@teste.com", senha="senha-forte-123", **extra):
        return self.client.post(reverse("usuarios:login"), {"username": email, "password": senha, **extra})

    def test_credenciais_validas_entram_e_vao_para_a_lista(self):
        resposta = self.entrar()

        self.assertRedirects(resposta, reverse("quadras:lista"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.usuario.pk)

    def test_email_nao_diferencia_maiusculas(self):
        self.entrar(email="  ALUNO@teste.com ")

        self.assertIn("_auth_user_id", self.client.session)

    def test_senha_errada_e_email_inexistente_dao_a_mesma_mensagem(self):
        senha_errada = self.entrar(senha="errada")
        email_inexistente = self.entrar(email="ninguem@teste.com")

        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(senha_errada, "E-mail ou senha incorretos.")
        self.assertContains(email_inexistente, "E-mail ou senha incorretos.")

    def test_volta_para_a_pagina_de_origem(self):
        destino = reverse("quadras:lista") + "?origem=login"
        resposta = self.entrar(next=destino)

        self.assertRedirects(resposta, destino)

    def test_nao_redireciona_para_site_externo(self):
        resposta = self.entrar(next="https://exemplo.com/")

        self.assertRedirects(resposta, reverse("quadras:lista"))

    def test_logout_encerra_a_sessao(self):
        self.client.force_login(self.usuario)

        self.client.post(reverse("usuarios:logout"))

        self.assertNotIn("_auth_user_id", self.client.session)
