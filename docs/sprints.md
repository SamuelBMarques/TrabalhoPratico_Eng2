# Planejamento das Sprints — Sistema de Reserva de Quadras

## 1. Equipe e Papéis
| Integrante | Papel na Sprint 1 |
|------------|-------------------|
| ... | Product Owner |
| ... | Scrum Master |
| Samuel | Desenvolvedor |
| Pedro Souza | Desenvolvedor |

## 2. Calendário e Milestones
| Sprint | Início | Fim | Objetivo | Milestone |
|--------|--------|-----|----------|-----------|
| 1 | 22/10/2026 | 04/11/2026 | Usuário consegue se cadastrar e o administrador consegue manter quadras e horários de funcionamento | [Sprint 1](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/2) |
| 2 | 05/11/2026 | 18/11/2026 | Usuário autenticado consegue consultar quadras e horários disponíveis e realizar uma reserva confirmada | [Sprint 2](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/3) |
| 3 | 19/11/2026 | 02/12/2026 | Usuário consegue acompanhar e cancelar suas reservas, e o administrador consegue gerenciar reservas e bloquear horários | [Sprint 3](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/4) |
| 4 | 03/12/2026 | 16/12/2026 | Testes, correções e apresentação | [Sprint 4](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/5) |

Todos os milestones: <https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestones>

## 3. Backlog por Sprint
### Sprint 1 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/2)
| História | Tarefas | Responsável | Issue |
|----------|---------|-------------|-------|
| H01 | Definir os dados do usuário (nome, e-mail, senha etc.) | Samuel | #30 |
| H01 | Implementar o cadastro no banco de dados | Samuel | #31 |
| H01 | Criar a tela de cadastro | Samuel | #32 |
| H01 | Testar o cadastro e a validação dos dados | ... | #33 |
| H10 | Implementar o cadastro de quadras | Pedro Souza | #26 |
| H10 | Implementar a edição de quadras | Pedro Souza | #27 |
| H10 | Implementar a exclusão ou desativação de quadras | Pedro Souza | #28 |
| H10 | Criar a interface de gerenciamento de quadras | ... | #34 |
| H10 | Testar o gerenciamento de quadras | ... | #29 |
| H11 | Definir os dados dos horários | ... | #18 |
| H11 | Implementar o cadastro dos horários de funcionamento | ... | #19 |
| H11 | Implementar a edição dos horários cadastrados | ... | #20 |
| H11 | Implementar a exclusão ou desativação de horários | ... | #21 |
| H11 | Verificar se os horários cadastrados são válidos | ... | #22 |
| H11 | Impedir horários duplicados ou conflitantes | ... | #23 |
| H11 | Criar a tela de gerenciamento de horários | ... | #24 |
| H11 | Testar o cadastro, a edição e a exclusão de horários | ... | #25 |
| H03 | Implementar a listagem de quadras | David | #3 |
| H03 | Criar a tela de visualização de quadras | David | #3 |
| H03 | Testar a visualização de quadras | David | #3 |

### Sprint 2 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/3)
O backlog da Sprint 2 foi implementado anteriormente pela equipe conforme o objetivo definido na tabela acima.

### Sprint 3 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/4)
| História | Tarefa | Responsável | Issue |
|----------|--------|-------------|-------|
| H07 | Cancelar reserva própria e liberar o horário | Kayo Xavier | #7 |
| H08 | Visualizar as próprias reservas | Kayo Xavier | #8 |
| H09 | Alterar data ou horário de uma reserva | Kayo Xavier | #17 |

As funcionalidades acima foram implementadas na branch `feat/reservas-7-8-17`, com testes automatizados para autorização, cancelamento, listagem e alteração de reservas. O commit e o pull request devem ser publicados no GitHub após a configuração da identidade e autenticação do Git.

### Sprint 4 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/5)
Reservada para testes finais, correções e apresentação.
