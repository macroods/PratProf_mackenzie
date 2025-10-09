## TST01 Reserva bem-sucedida

**Caso de uso em que se baseia:** Reservar mesa

**Cenário:** Fluxo principal

**Preparação:**

a) O usuário deve estar cadastrado no sistema, com os seguintes dados: Nome, email, senha.

**Passos para execução do teste:**

1. Acessar a página inicial da aplicação (login).
2. Entrar com as credenciais corretas.
3. Escolher um horário disponível (azul) de um restaurante.
4. Digitar o número de pessoas e clicar em "confirmar reserva".
5. Verificar os dados da reserva feita na página "minhas reservas".

**Resultado esperado:**

a) Dados da reserva inseridos na tabela na página "minhas reservas" com os seguintes dados:
Nome do restaurante, data da reserva, horário, n° de pessoas, e botão "cancelar".

**Resultado obtido:**

(x) Sucesso
( ) Não executado
( ) Falha
( ) Cancelado

**Descrição do resultado obtido:**

O sistema só permite reserva de pessoas cadastradas, e as reservas só são feitas corretamente em horários disponíveis.

**Data da última execução do teste:**

09/10/2025