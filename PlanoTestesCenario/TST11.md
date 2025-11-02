## TST11 Nome do restaurante já cadastrado

**Caso de uso em que se baseia:** Cadastrar restaurante

**Cenário:** Nome duplicado (negativo)

**Preparação:**

a) Existe um restaurante cadastrado com o nome "La Pasta Bella".

**Passos para execução do teste:**

1. Acessar a página de login, clicar em "Cadastrar Restaurante".
2. Preencher Nome = "La Pasta Bella" (mesmo nome), Email, Senha, Horários disponíveis.
3. Clicar em "Cadastrar Restaurante".

**Resultado esperado:**

a) Exibir aviso de erro ("Nome de restaurante já existe").  
b) Nenhum novo registro deve ser criado com esse nome duplicado.

**Resultado obtido:**

( ) Sucesso  
( ) Não executado  
(X) Falha  
( ) Cancelado

**Descrição do resultado obtido:**

A página "Internal Server Error" é carregada. A função de apresentar mensagem de erro não está implementada.

**Data da execução:** 

02/11/2025