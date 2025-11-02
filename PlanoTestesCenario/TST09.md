## TST09 Cadastro restaurante bem‑sucedido

**Caso de uso em que se baseia:** Cadastrar restaurante

**Cenário:** Fluxo principal

**Preparação:**

a) Nenhum restaurante com o mesmo email ou nome deve existir no banco.

**Passos para execução do teste:**

1. Acessar a página de login e clicar em "Cadastrar Restaurante".
2. Preencher Nome, Email (válido), Senha e Horários disponíveis.
3. Clicar em "Cadastrar Restaurante".

**Resultado esperado:**

a) Redirecionamento para a página de login.  
b) Novo restaurante inserido na tabela `restaurantes` com campos (nome, email, senha, horario_disponivel).  
c) Restaurante aparece na lista de restaurantes para os clientes.

**Resultado obtido:**

(X) Sucesso  
( ) Não executado  
( ) Falha  
( ) Cancelado

**Descrição do resultado obtido:**

---

**Data da execução:** 

02/11/2025