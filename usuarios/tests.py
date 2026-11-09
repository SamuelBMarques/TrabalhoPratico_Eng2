from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class CadastroUsuarioTests(TestCase):
    """US01, subissue #33: cadastro e validação pela interface."""

    def setUp(self):
        self.url = reverse("usuarios:cadastro")
        self.dados = {
            "nome": "  Aluno Teste  ",
            "email": "  ALUNO@teste.com  ",
            "senha": "Uma-senha-forte-789!",
            "confirmar_senha": "Uma-senha-forte-789!",
        }

    def test_abrir_formulario_nao_cria_conta(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "usuarios/cadastro.html")
        self.assertFalse(get_user_model().objects.exists())

    def test_cadastro_valido_persiste_dados_e_hash_da_senha(self):
        resposta = self.client.post(self.url, self.dados, follow=True)

        usuario = get_user_model().objects.get()
        self.assertEqual(usuario.nome, "Aluno Teste")
        self.assertEqual(usuario.email, "aluno@teste.com")
        self.assertNotEqual(usuario.password, self.dados["senha"])
        self.assertTrue(usuario.check_password(self.dados["senha"]))
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
        self.assertRedirects(resposta, self.url)
        self.assertContains(resposta, "Cadastro realizado com sucesso!")

    def test_campos_obrigatorios_nao_podem_ficar_vazios(self):
        for campo in self.dados:
            with self.subTest(campo=campo):
                resposta = self.client.post(self.url, {**self.dados, campo: ""})

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(campo, resposta.context["form"].errors)
                self.assertFalse(get_user_model().objects.exists())

    def test_nome_apenas_com_espacos_e_email_invalido_sao_recusados(self):
        for campo, valor in [("nome", "   "), ("email", "email-sem-arroba")]:
            with self.subTest(campo=campo):
                resposta = self.client.post(self.url, {**self.dados, campo: valor})

                self.assertIn(campo, resposta.context["form"].errors)
                self.assertFalse(get_user_model().objects.exists())

    def test_email_duplicado_nao_cria_conta_nem_altera_a_existente(self):
        usuario = get_user_model().objects.create_user(
            email="aluno@teste.com", nome="Original", password="Senha-original-456!",
        )
        resposta = self.client.post(self.url, self.dados)

        self.assertContains(resposta, "Já existe uma conta cadastrada com este e-mail.")
        self.assertEqual(get_user_model().objects.count(), 1)
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, "Original")
        self.assertTrue(usuario.check_password("Senha-original-456!"))

    def test_senhas_diferentes_nao_criam_conta(self):
        resposta = self.client.post(self.url, {**self.dados, "confirmar_senha": "Outra-senha-456!"})

        self.assertContains(resposta, "As senhas não coincidem.")
        self.assertIn("confirmar_senha", resposta.context["form"].errors)
        self.assertFalse(get_user_model().objects.exists())

    def test_senhas_fracas_sao_recusadas(self):
        for senha in ["aZ!2", "123456789123", "password"]:
            with self.subTest(senha=senha):
                resposta = self.client.post(self.url, {
                    **self.dados, "senha": senha, "confirmar_senha": senha,
                })

                self.assertIn("senha", resposta.context["form"].errors)
                self.assertFalse(get_user_model().objects.exists())

    def test_campos_enviados_nao_concedem_privilegios_administrativos(self):
        self.client.post(self.url, {**self.dados, "is_staff": "on", "is_superuser": "on"})

        usuario = get_user_model().objects.get()
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

    def test_envio_sem_token_csrf_e_recusado(self):
        resposta = Client(enforce_csrf_checks=True).post(self.url, self.dados)

        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(get_user_model().objects.exists())


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
