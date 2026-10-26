# Requisitos — Sistema de Reserva de Quadras

- **Disciplina:** Engenharia de Software II
- **Projeto:** Sistema de Reserva de Quadras
- **Versão do documento:** 2.0
- **Objetivo da versão:** definir os requisitos para orientar o desenvolvimento e a entrega principal prevista para dezembro.

---

## 1. Visão do Produto

O Sistema de Reserva de Quadras centraliza a consulta de quadras esportivas e o agendamento de horários, resolvendo os conflitos de agendamento e a necessidade de controles manuais. Destina-se a usuários que desejam consultar disponibilidade e reservar quadras, e a administradores que precisam manter o cadastro das quadras, seus horários de funcionamento e as reservas. Seu diferencial é validar a disponibilidade no momento da reserva, garantindo que duas reservas válidas nunca ocupem o mesmo horário da mesma quadra, e oferecer ao administrador controle sobre a disponibilidade (funcionamento, desativação de quadras e bloqueios).

## 2. Papéis de Usuário

| Papel | Descrição |
|-------|-----------|
| Usuário | Pessoa que utiliza o sistema para consultar quadras, verificar disponibilidade e realizar ou acompanhar suas próprias reservas. |
| Administrador | Pessoa autorizada a manter o cadastro das quadras, configurar horários de funcionamento e consultar ou gerenciar as reservas do sistema. Possui permissões diferentes das de um usuário comum. |

## 3. Histórias de Usuário

### H01 — Cadastro de usuário (Essencial)
**Como** usuário, **eu quero** criar uma conta informando meus dados **para** poder fazer e acompanhar reservas de quadras.

**Critérios de aceitação:**
- [ ] O cadastro solicita, no mínimo, nome, e-mail e senha.
- [ ] Os campos obrigatórios e o formato do e-mail são validados.
- [ ] Não é possível cadastrar mais de uma conta com o mesmo e-mail.
- [ ] A senha não é armazenada em texto puro.
- [ ] Em caso de dados inválidos, o sistema informa o problema sem concluir o cadastro.

### H02 — Login (Essencial)
**Como** usuário cadastrado, **eu quero** entrar no sistema com e-mail e senha **para** acessar as funcionalidades restritas e minhas reservas.

**Critérios de aceitação:**
- [ ] As credenciais informadas são validadas.
- [ ] O acesso é concedido somente quando as credenciais são válidas.
- [ ] Em caso de falha, é exibida uma mensagem adequada, sem revelar informações sensíveis.
- [ ] As funcionalidades restritas exigem autenticação.

### H03 — Visualizar quadras (Essencial)
**Como** usuário, **eu quero** ver as quadras cadastradas **para** escolher qual delas reservar.

**Critérios de aceitação:**
- [ ] Cada quadra exibe informações que permitam identificá-la: nome, descrição, tipo ou modalidades aceitas e situação.
- [ ] A listagem permite identificar quais quadras podem ser reservadas.
- [ ] Quadras desativadas não são oferecidas para novas reservas.
- [ ] A listagem reflete os dados cadastrados no sistema.

### H04 — Consultar horários (Essencial)
**Como** usuário, **eu quero** consultar os horários disponíveis de uma quadra em uma data **para** identificar um período livre para reservar.

**Critérios de aceitação:**
- [ ] A consulta considera a quadra e a data escolhidas.
- [ ] A consulta considera os horários de funcionamento cadastrados.
- [ ] Horários já reservados ou bloqueados não aparecem como disponíveis.
- [ ] Quando não há horários disponíveis, o sistema exibe uma indicação.
- [ ] A disponibilidade apresentada é validada novamente no momento da criação da reserva.

### H05 — Realizar reserva (Essencial)
**Como** usuário autenticado, **eu quero** reservar uma quadra em uma data e horário disponíveis **para** garantir o uso do espaço sem conflitos com outras pessoas.

**Critérios de aceitação:**
- [ ] A reserva fica associada ao usuário, à quadra, à data e ao horário selecionados.
- [ ] A disponibilidade é validada antes de registrar a reserva.
- [ ] Não é possível concluir duas reservas conflitantes para a mesma quadra.
- [ ] Não é possível reservar fora do horário de funcionamento ou durante um bloqueio.
- [ ] Se o horário deixar de estar disponível antes da confirmação, a operação é recusada e o usuário é informado.
- [ ] A reserva é persistida no banco de dados.

### H06 — Confirmar reserva (Essencial)
**Como** usuário, **eu quero** receber a confirmação da reserva realizada **para** ter certeza de que o agendamento foi registrado.

**Critérios de aceitação:**
- [ ] A reserva possui um status registrado no sistema.
- [ ] A confirmação apresenta informações suficientes para identificar a reserva, incluindo quadra, data e horário.
- [ ] A confirmação só é apresentada como bem-sucedida após o registro da reserva.
- [ ] A confirmação exibida no sistema é obrigatória para o fluxo principal; o envio de mensagem externa é tratado em H15.

### H07 — Cancelar reserva (Essencial)
**Como** usuário, **eu quero** cancelar uma reserva minha **para** liberar o horário quando não puder comparecer.

**Critérios de aceitação:**
- [ ] O sistema verifica se a reserva existe e se pode ser cancelada, conforme as regras de cancelamento definidas pelo projeto.
- [ ] Um usuário comum só pode cancelar as próprias reservas.
- [ ] Um administrador pode cancelar ou gerenciar reservas conforme suas permissões.
- [ ] Após o cancelamento, o status da reserva é atualizado.
- [ ] O horário volta a ficar disponível quando não houver outra restrição aplicável.
- [ ] O sistema informa o resultado da operação.

### H08 — Visualizar minhas reservas (Essencial)
**Como** usuário autenticado, **eu quero** consultar minhas reservas **para** acompanhar meus agendamentos.

**Critérios de aceitação:**
- [ ] A listagem apresenta quadra, data, horário e status de cada reserva.
- [ ] O usuário visualiza somente as reservas associadas à própria conta.
- [ ] A listagem reflete as alterações de status realizadas no sistema.
- [ ] Caso não existam reservas, o sistema informa que a lista está vazia.

### H09 — Alterar reserva (Desejável)
**Como** usuário, **eu quero** alterar a data ou o horário de uma reserva existente **para** ajustar meu agendamento sem precisar cancelar e refazer a reserva.

**Critérios de aceitação:**
- [ ] O sistema verifica se o usuário tem permissão para alterar a reserva.
- [ ] A nova data e o novo horário são válidos e estão disponíveis.
- [ ] A alteração não gera conflitos com outras reservas.
- [ ] Se a alteração não puder ser realizada, a reserva original é preservada.
- [ ] Após uma alteração bem-sucedida, o sistema apresenta os dados atualizados.

### H10 — Gerenciar quadras (Essencial)
**Como** administrador, **eu quero** cadastrar, editar e desativar quadras **para** manter atualizadas as quadras oferecidas para reserva.

**Critérios de aceitação:**
- [ ] Somente administradores podem realizar operações de gerenciamento de quadras.
- [ ] O cadastro exige os dados necessários para identificar a quadra.
- [ ] O administrador pode editar os dados de uma quadra cadastrada.
- [ ] A remoção ou desativação considera a existência de reservas relacionadas.
- [ ] Quando a exclusão física puder comprometer o histórico ou a integridade dos dados, a quadra é desativada em vez de excluída.
- [ ] Quadras desativadas não aceitam novas reservas.

### H11 — Gerenciar horários de funcionamento (Essencial)
**Como** administrador, **eu quero** definir e manter os horários de funcionamento de cada quadra **para** que a disponibilidade seja calculada corretamente.

**Critérios de aceitação:**
- [ ] Cada horário está associado a uma quadra e contém, no mínimo, dia da semana, horário de início e horário de fim.
- [ ] Os dados são validados e o horário de início é anterior ao horário de fim.
- [ ] O sistema impede horários duplicados ou conflitantes para a mesma quadra.
- [ ] O administrador pode cadastrar, editar e desativar horários.
- [ ] Alterações nos horários de funcionamento não tornam válidas novas reservas fora dos períodos permitidos.
- [ ] Alterações que afetem reservas já existentes são tratadas de forma controlada, conforme a decisão registrada na seção 8.

### H12 — Gerenciar reservas (Importante)
**Como** administrador, **eu quero** consultar e gerenciar as reservas cadastradas **para** acompanhar e controlar a ocupação das quadras.

**Critérios de aceitação:**
- [ ] O administrador consulta reservas de diferentes usuários.
- [ ] A listagem apresenta usuário, quadra, data, horário e status.
- [ ] A listagem permite filtros por data, quadra e status.
- [ ] O administrador pode alterar o status de uma reserva conforme as regras do sistema.
- [ ] As operações verificam as permissões administrativas.
- [ ] As alterações preservam a consistência dos dados e a disponibilidade das quadras.

### H13 — Bloquear horário (Importante)
**Como** administrador, **eu quero** bloquear períodos de uma quadra **para** impedir novas reservas durante manutenção ou eventos.

**Critérios de aceitação:**
- [ ] O bloqueio está associado a uma quadra, data, horário de início e horário de fim.
- [ ] O sistema permite registrar, opcionalmente, o motivo do bloqueio.
- [ ] O período é validado para impedir intervalos inválidos ou conflitantes.
- [ ] O sistema verifica se existem reservas no período escolhido.
- [ ] Havendo reservas conflitantes, o bloqueio não é concluído silenciosamente: o administrador é informado e deve decidir conforme as regras do projeto.
- [ ] Novas reservas não podem ocorrer durante o período bloqueado.
- [ ] O administrador pode consultar e remover bloqueios cadastrados.

### H14 — Histórico de reservas (Desejável)
**Como** usuário, **eu quero** consultar o histórico das minhas reservas **para** rever agendamentos passados, concluídos e cancelados.

**Critérios de aceitação:**
- [ ] O histórico inclui reservas concluídas, canceladas e passadas.
- [ ] Cada registro apresenta quadra, data, horário e status.
- [ ] A consulta oferece filtros por data, quadra e status.
- [ ] O usuário visualiza somente o próprio histórico.
- [ ] A consulta do histórico não permite alteração indevida dos registros.

### H15 — Notificações (Desejável)
**Como** usuário, **eu quero** receber notificações sobre minhas reservas **para** acompanhar confirmações, alterações e cancelamentos sem precisar consultar a lista.

**Critérios de aceitação:**
- [ ] São geradas notificações para confirmação, alteração e cancelamento de reservas.
- [ ] Cada notificação está associada ao usuário correto.
- [ ] As mensagens apresentam informações suficientes para identificar a ação realizada.
- [ ] As notificações podem ser marcadas como lidas.
- [ ] Na entrega principal, a confirmação apresentada na própria aplicação é suficiente; as notificações complementares são implementadas posteriormente.
- [ ] O canal de notificação (por exemplo, notificação interna ou e-mail) é definido pela equipe antes da implementação.

## 4. Priorização de Requisitos

As prioridades indicam a importância de cada história para a entrega principal, e não a ordem numérica das histórias.

* **Essencial** — sem isso o sistema não faz sentido: é necessária para que o fluxo de reserva possa ser demonstrado.
* **Importante** — agrega muito valor e melhora a operação, mas o sistema funciona sem.
* **Desejável** — será feito se sobrar tempo, sem comprometer o fluxo principal.
* **Fora do escopo** — não será feito neste semestre.

| Prioridade | Histórias |
|------------|-----------|
| Essencial | H01, H02, H03, H04, H05, H06, H07, H08, H10, H11 |
| Importante | H12, H13 |
| Desejável | H09, H14, H15 |
| Fora do escopo | Nenhuma das histórias H01–H15; ver itens na seção 4.2 |

A classificação deve ser validada pela equipe e pode ser revisada durante o desenvolvimento, sempre registrando a mudança neste documento.

### 4.1 Justificativa por história

| História | Funcionalidade | Prioridade | Justificativa |
|----------|----------------|------------|---------------|
| H01 | Cadastro de usuário | Essencial | Necessário para identificar quem realiza as reservas. |
| H02 | Login | Essencial | Necessário para proteger e personalizar o acesso. |
| H03 | Visualizar quadras | Essencial | Permite escolher a quadra que será reservada. |
| H04 | Consultar horários | Essencial | Permite identificar períodos disponíveis. |
| H05 | Realizar reserva | Essencial | É a funcionalidade central do sistema. |
| H06 | Confirmar reserva | Essencial | Dá retorno ao usuário e conclui o fluxo principal. |
| H07 | Cancelar reserva | Essencial | Permite liberar horários e administrar compromissos. |
| H08 | Visualizar minhas reservas | Essencial | Permite acompanhar os próprios agendamentos. |
| H09 | Alterar reserva | Desejável | Conveniente, mas não indispensável ao fluxo mínimo. |
| H10 | Gerenciar quadras | Essencial | Necessário para manter as quadras disponíveis no sistema. |
| H11 | Gerenciar horários | Essencial | Necessário para calcular a disponibilidade corretamente. |
| H12 | Gerenciar reservas | Importante | Facilita a operação administrativa, mas pode ser ampliado depois do fluxo principal. |
| H13 | Bloquear horário | Importante | Importante para manutenção e eventos; pode ser desenvolvido após a disponibilidade básica. |
| H14 | Histórico de reservas | Desejável | Complementa a consulta das reservas atuais. |
| H15 | Notificações | Desejável | Melhora a comunicação, mas pode ser adiada se a confirmação interna estiver implementada. |

### 4.2 Fora do escopo

Nenhuma das histórias H01–H15 foi descartada até o momento. As histórias *desejáveis* (H09, H14, H15) passam a ser **fora do escopo** se não tiverem sido iniciadas até a revisão da Sprint 3 (ver `sprints.md`).

Além disso, os itens abaixo **não serão feitos neste semestre** (proposta inicial, a ser validada pela equipe):

- Pagamento online ou cobrança pela reserva.
- Aplicativo móvel nativo (o sistema será acessado pelo navegador).
- Recuperação e redefinição de senha.
- Reservas recorrentes (por exemplo, toda semana no mesmo horário).
- Lista de espera para horários já reservados.

## 5. Requisitos Não Funcionais

Os requisitos a seguir descrevem características de qualidade e restrições que orientam a implementação. Os critérios mensuráveis podem ser refinados pela equipe conforme a arquitetura e as tecnologias escolhidas.

| ID | Requisito |
|----|-----------|
| RNF01 | **Segurança e autenticação.** O sistema deve proteger o acesso às funcionalidades restritas, exigir autenticação quando necessário e armazenar senhas de forma segura, utilizando um mecanismo apropriado de hash de senhas. |
| RNF02 | **Controle de permissões.** O sistema deve distinguir usuários comuns e administradores. As permissões devem ser verificadas no processamento das operações, e não apenas pela interface apresentada. |
| RNF03 | **Integridade dos dados.** O sistema deve manter a consistência dos dados de usuários, quadras, horários e reservas. As operações de reserva devem impedir conflitos, inclusive quando houver tentativas simultâneas de reservar o mesmo horário. |
| RNF04 | **Persistência.** Os dados necessários ao funcionamento do sistema devem ser armazenados de forma persistente, continuando disponíveis após o encerramento e a reinicialização da aplicação. |
| RNF05 | **Usabilidade.** As telas devem apresentar informações de forma clara, com campos identificados, mensagens de erro compreensíveis e retorno visível após operações importantes, como cadastro, login, reserva e cancelamento. |
| RNF06 | **Manutenibilidade.** O código deve ser organizado de forma modular, com responsabilidades bem definidas, para facilitar correções, testes e inclusão de funcionalidades. |
| RNF07 | **Testabilidade.** As funcionalidades principais devem possuir testes que verifiquem tanto os fluxos válidos quanto os casos de erro, especialmente autenticação, consulta de disponibilidade, criação de reservas e cancelamento. |
| RNF08 | **Compatibilidade.** A aplicação deve funcionar no ambiente e nos navegadores definidos pela equipe para a demonstração do projeto. Os ambientes suportados devem ser documentados no README. |
| RNF09 | **Privacidade.** O sistema deve limitar a visualização de dados pessoais e de reservas de acordo com as permissões de cada perfil, evitando que usuários comuns acessem informações privadas de outros usuários. |
| RNF10 | **Tratamento de erros.** Falhas de validação, indisponibilidade de horários e erros no processamento devem ser tratados de maneira controlada, informando o usuário sem expor senhas, credenciais ou detalhes internos desnecessários. |


