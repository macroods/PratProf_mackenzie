## TST03 Email já cadastrado

**Caso de uso em que se baseia:** Fazer cadastro de cliente

**Cenário:** Fluxo principal

**Preparação:**

a) O usuário deve estar cadastrado no sistema, com os seguintes dados: Nome, email, senha.

**Passos para execução do teste:**

1. Acessar a página inicial da aplicação (login).
2. Entrar com as credenciais corretas de um cliente já registrado.
4. Clicar em "Cadastrar".

**Resultado esperado:**

a) Um aviso vermelho abaixo da caixa de entrada dizendo "Email já cadastrado".
b) O cliente não deve ser registrado novamente no banco de dados.

**Resultado obtido:**

(x) Sucesso
( ) Não executado
( ) Falha
( ) Cancelado

**Descrição do resultado obtido:**

O sistema mostra o aviso corretamente e não registra o cliente no banco de dados.

**Data da última execução do teste:**

14/10/2025