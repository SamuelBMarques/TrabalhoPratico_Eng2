# Planejamento das Sprints — Sistema de Reserva de Quadras

## 1. Equipe e Papéis
| Integrante | Papel na Sprint 1 |
|------------|-------------------|
| ... | Product Owner |
| Samuel Marques | Scrum Master |
| Samuel Marques| Desenvolvedor |
| Pedro Souza | Desenvolvedor |
| Pedro Boseja | Desenvolvedor |
| David | Desenvolvedor |
| Matheus Cardoso| Desenvolvedor |
| Kayo Xavier| Desenvolvedor |

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
| História | Tarefas | Issue |
|----------|---------|-------|
| H01 | Definir os dados do usuário (nome, e-mail, senha etc.) |#30 |
| H01 | Implementar o cadastro no banco de dados |#31 |
| H01 | Criar a tela de cadastro |#32 |
| H01 | Testar o cadastro e a validação dos dados |#33 |
| H10 | Implementar o cadastro de quadras |#26 |
| H10 | Implementar a edição de quadras |#27 |
| H10 | Implementar a exclusão ou desativação de quadras |#28 |
| H10 | Criar a interface de gerenciamento de quadras |#34 |
| H10 | Testar o gerenciamento de quadras |#29 |
| H11 | Definir os dados dos horários |#18 |
| H11 | Implementar o cadastro dos horários de funcionamento |#19 |
| H11 | Implementar a edição dos horários cadastrados |#20 |
| H11 | Implementar a exclusão ou desativação de horários |#21 |
| H11 | Verificar se os horários cadastrados são válidos |#22 |
| H11 | Impedir horários duplicados ou conflitantes |#23 |
| H11 | Criar a tela de gerenciamento de horários |#24 |
| H11 | Testar o cadastro, a edição e a exclusão de horários |#25 |
| H03 | Implementar a listagem de quadras |#3 |
| H03 | Criar a tela de visualização de quadras |#3 |
| H03 | Testar a visualização de quadras |#3 |

### Sprint 2 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/3)
| História | Tarefas | Issue |
|----------|---------|-------|
| H11 | Implementar a exclusão ou desativação de horários |#21 |
| H11 | Verificar se os horários cadastrados são válidos |#22 |
| H11 | Impedir horários duplicados ou conflitantes |#23 |
| H11 | Criar a tela de gerenciamento de horários |#24 |
| H11 | Testar o cadastro, a edição e a exclusão de horários |#25 |
| H02 | Configurar a autenticação por e-mail e senha |#48 |
| H02 | Criar a tela de login |#49 |
| H02 | Implementar o logout e o retorno à página de origem |#50 |
| H02 | Testar o login e o logout |#51 |
| H04 | Definir os dados de reservas e bloqueios |#52 |
| H04 | Calcular os horários disponíveis da quadra |#53 |
| H04 | Criar a tela de consulta de horários |#54 |
| H04 | Testar a consulta de horários |#55 |
| H05 | Implementar a criação da reserva com revalidação do horário |#56 |
| H05 | Impedir reservas conflitantes no banco de dados |#57 |
| H05 | Adicionar a ação de reservar na tela de horários |#58 |
| H05 | Testar a criação de reservas |#59 |
| H06 | Registrar o status da reserva |#60 |
| H06 | Exibir a confirmação após o registro da reserva |#61 |
| H06 | Testar a confirmação da reserva |#62 |

### Sprint 3 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/4)
| História | Tarefas | Issue |
|----------|---------|-------|
| H07 | Implementar a lógica de cancelamento de reservas e verificar permissões | #68 |
| H07 | Criar a ação e a interface para cancelar uma reserva | #69 |
| H07 | Atualizar a disponibilidade após o cancelamento | #70 |
| H07 | Testar o cancelamento, as permissões e a liberação do horário | #71 |
| H08 | Implementar a consulta das reservas do usuário autenticado | #72 |
| H08 | Criar a tela de visualização das minhas reservas | #73 |
| H08 | Testar a listagem, a privacidade e o estado vazio | #74 |
| H09 | Implementar a alteração de data ou horário com validação de disponibilidade | #75 |
| H09 | Criar a interface para alterar uma reserva | #76 |
| H09 | Garantir a preservação da reserva original quando a alteração falhar | #77 |
| H09 | Testar as alterações, permissões e conflitos | #78 |
| H12 | Implementar a consulta administrativa de reservas | #79 |
| H12 | Implementar filtros por data, quadra e status | #80 |
| H12 | Implementar a alteração do status de uma reserva com controle de permissões | #81 |
| H12 | Criar a interface administrativa de gerenciamento de reservas | #82 |
| H12 | Testar a consulta, os filtros e o gerenciamento de reservas | #83 |
| H13 | Criar a estrutura de dados e as operações de cadastro, consulta e remoção de bloqueios | #84 |
| H13 | Validar períodos de bloqueio e identificar reservas conflitantes | #85 |
| H13 | Integrar os bloqueios ao cálculo de disponibilidade e à criação de reservas | #86 |
| H13 | Criar a interface administrativa para gerenciar bloqueios | #87 |
| H13 | Testar o cadastro, a validação, os conflitos e a remoção de bloqueios | #88 |

### Sprint 4 — [milestone](https://github.com/SamuelBMarques/TrabalhoPratico_Eng2/milestone/5)
O backlog da Sprint 4 será detalhado no planejamento da própria sprint.