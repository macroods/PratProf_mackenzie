## TST02 Quantidade de pessoas permitidas na reserva

**Caso de uso em que se baseia:** Reservar mesa

**Cenário:** Fluxo principal

**Preparação:**

a) O usuário deve estar cadastrado no sistema, com os seguintes dados: Nome, email, senha.

**Passos para execução do teste:**

1. Acessar a página inicial da aplicação (login).
2. Entrar com as credenciais corretas.
3. Escolher um horário disponível (azul) de um restaurante.
4. Digitar o número de pessoas **menor que um** e clicar em "confirmar reserva".

**Resultado esperado:**

a) Um aviso dizendo "Selecione um valor que não seja menor que 1".
b) A reserva não aparece na tabela de "minhas reservas".

**Resultado obtido:**

(x) Sucesso
( ) Não executado
( ) Falha
( ) Cancelado

**Descrição do resultado obtido:**

O sistema só permite números acima de 1, e a reserva não é feita caso contrário.

**Data da última execução do teste:**

09/10/2025