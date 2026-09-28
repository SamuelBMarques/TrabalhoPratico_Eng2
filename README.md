# 🏀 Sistema de Reserva de Quadras

> Trabalho da disciplina **Engenharia de Software II**

Aplicação para gerenciar a **reserva das quadras esportivas** da faculdade (poliesportiva, futsal, vôlei, basquete etc.). O objetivo é acabar com conflitos de horário e com o controle manual em papel ou planilha.

---

## 📌 Sumário

- [Ideia geral do projeto](#-ideia-geral-do-projeto)
- [Descrição geral do sistema](#-descrição-geral-do-sistema)
- [Perfis de usuário](#-perfis-de-usuário)
- [Funcionalidades](#-funcionalidades)
- [Histórias de usuário](#-histórias-de-usuário)
- [Integrantes da equipe](#-integrantes-da-equipe)
- [Quadro Kanban](#-quadro-kanban)

---

## 💡 Ideia geral do projeto

Na maioria das faculdades, o uso das quadras é combinado de forma manual: na secretaria, em cadernos de agendamento, por mensagens ou por planilhas. Isso costuma causar:

- **conflitos de horário** (dois grupos na mesma quadra ao mesmo tempo);
- **quadras ociosas**, porque ninguém sabe que estão livres;
- **falta de transparência** sobre quem reservou e quando;
- **retrabalho** para o setor responsável, que precisa conferir tudo à mão.

A proposta é um sistema centralizado em que alunos, professores e atléticas consultam a disponibilidade das quadras e fazem suas reservas de forma simples. A administração controla as quadras, os horários de funcionamento e os bloqueios (manutenção, jogos e eventos).

---

## 🖥️ Descrição geral do sistema

O **Sistema de Reserva de Quadras** é uma aplicação em que:

1. O usuário **cria uma conta** e **faz login** com e-mail e senha.
2. Ele **consulta as quadras disponíveis**, com informações como tipo, modalidades aceitas e capacidade.
3. Ele escolhe uma quadra, **consulta os horários livres** e **faz a reserva** para uma data e horário.
4. O sistema **confirma a reserva** e **envia notificações** sobre confirmações, alterações e cancelamentos.
5. O usuário pode **ver, alterar ou cancelar** suas reservas e consultar o **histórico** de uso.
6. O **administrador** cadastra e mantém as quadras, define os horários de funcionamento, **bloqueia horários** (manutenção ou eventos) e gerencia todas as reservas do sistema.

### Regras de negócio principais

- Uma quadra não pode ter duas reservas no mesmo horário.
- Não é possível reservar horários bloqueados pelo administrador nem fora do horário de funcionamento.
- Só o dono da reserva (ou um administrador) pode alterá-la ou cancelá-la.
- Toda criação, alteração ou cancelamento de reserva gera uma notificação para o usuário.

---

## 👥 Perfis de usuário

| Perfil | Descrição |
|---|---|
| **Usuário** | Aluno, professor ou membro de atlética. Consulta as quadras, faz e gerencia as próprias reservas. |
| **Administrador** | Setor de esportes da faculdade. Gerencia quadras, horários, bloqueios e todas as reservas. |

---

## ⚙️ Funcionalidades

**Usuário**
- Cadastro e login
- Visualização das quadras e dos horários disponíveis
- Criação, alteração e cancelamento de reservas
- Consulta das reservas atuais e do histórico
- Recebimento de notificações

**Administrador**
- CRUD de quadras (cadastrar, editar, remover)
- Definição dos horários de funcionamento de cada quadra
- Bloqueio de horários para manutenção ou eventos
- Visualização e gerenciamento de todas as reservas

---

## 📝 Histórias de usuário

| ID | História | Descrição |
|---|---|---|
| **US01** | Cadastro de usuário | Como usuário, quero criar uma conta no sistema, para poder realizar reservas de quadras. |
| **US02** | Login | Como usuário, quero entrar no sistema com meu e-mail e senha, para acessar minhas funcionalidades. |
| **US03** | Visualizar quadras | Como usuário, quero visualizar as quadras disponíveis, para escolher onde quero jogar. |
| **US04** | Consultar horários | Como usuário, quero consultar os horários disponíveis de uma quadra, para escolher um horário adequado. |
| **US05** | Realizar reserva | Como usuário, quero reservar uma quadra em uma data e horário, para garantir aquele horário para meu uso. |
| **US06** | Confirmar reserva | Como usuário, quero receber a confirmação da minha reserva, para ter certeza de que o agendamento foi realizado. |
| **US07** | Cancelar reserva | Como usuário, quero cancelar uma reserva, para liberar o horário caso eu não possa comparecer. |
| **US08** | Visualizar minhas reservas | Como usuário, quero visualizar minhas reservas, para acompanhar meus agendamentos. |
| **US09** | Alterar reserva | Como usuário, quero alterar a data ou o horário de uma reserva, para adequá-la à minha disponibilidade. |
| **US10** | Gerenciar quadras | Como administrador, quero cadastrar, editar e remover quadras, para manter as quadras disponíveis no sistema atualizadas. |
| **US11** | Gerenciar horários | Como administrador, quero definir os horários disponíveis para cada quadra, para controlar os períodos de funcionamento. |
| **US12** | Gerenciar reservas | Como administrador, quero visualizar e gerenciar todas as reservas, para organizar o uso das quadras. |
| **US13** | Bloquear horário | Como administrador, quero bloquear horários de uma quadra, para impedir reservas durante manutenção ou eventos. |
| **US14** | Histórico de reservas | Como usuário, quero consultar o histórico das minhas reservas, para saber quais quadras e horários já utilizei. |
| **US15** | Notificação | Como usuário, quero receber notificações sobre minhas reservas, para ser informado sobre confirmações, alterações ou cancelamentos. |

---

## 👨‍💻 Integrantes da equipe

| Nome |
|---|
| David |
| Kayo Xavier |
| Matheus Cardoso |
| Pedro Souza |
| Samuel Marques |

---

## 📋 Quadro Kanban

O andamento das tarefas é acompanhado no quadro Kanban do GitHub Projects:

🔗 **[Acessar o quadro Kanban](https://github.com/users/SamuelBMarques/projects/2/views/1)**

---

<p align="center">Engenharia de Software II</p>
