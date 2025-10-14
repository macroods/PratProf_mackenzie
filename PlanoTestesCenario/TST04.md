## TST04 Cancelamento de reserva

**Caso de uso em que se baseia:** Cancelar reserva

**Cenário:** Fluxo principal

**Preparação:**

a) O usuário deve estar cadastrado no sistema, com os seguintes dados: Nome, email, senha.
b) O usuário deve ter realizado pelo menos uma reserva bem-sucedida.

**Passos para execução do teste:**

1. Acessar a página de "Minhas reservas".
2. Clicar no botão (x) de cancelar reserva.

**Resultado esperado:**

a) A reserva é removida do banco de dados.
b) A tabela de reservas é atualizada sem a reserva cancelada.

**Resultado obtido:**

(x) Sucesso
( ) Não executado
( ) Falha
( ) Cancelado

**Descrição do resultado obtido:**

O sistema deleta a reserva do banco  de dados e a tabela é atualizada corretamente.

**Data da última execução do teste:**

14/10/2025