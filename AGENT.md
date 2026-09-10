# agent.md

## 1. Propósito deste arquivo

Este arquivo contém as regras obrigatórias para qualquer IA, agente de código ou assistente que trabalhe neste repositório.

O objetivo é impedir que o projeto fuja de sua proposta acadêmica e didática.

Antes de criar, alterar, refatorar ou excluir qualquer código, a IA deve ler este documento e considerar suas instruções como parte dos requisitos do projeto.

Quando houver conflito entre uma sugestão genérica de engenharia de software e este documento, **este documento deve prevalecer**, exceto quando uma instrução explícita do usuário determinar o contrário.

---

# 2. Visão geral do projeto

Este projeto representa um sistema simples para uma clínica veterinária.

O sistema deve permitir o gerenciamento de:

- animais;
- responsáveis pelos animais;
- atendimentos veterinários;
- tipos de serviço;
- valores cobrados;
- descontos;
- acréscimos;
- histórico de atendimentos;
- operações sobre listas de animais;
- consultas e cálculos relacionados aos atendimentos.

O projeto existe principalmente para o aprendizado e prática de:

- Python;
- Pytest;
- Test-Driven Development (TDD);
- testes unitários;
- orientação a objetos;
- modelagem de domínio;
- regras de negócio;
- manipulação de listas;
- refatoração segura;
- separação de responsabilidades;
- código simples e testável.

Este projeto **não tem como objetivo ser um sistema veterinário completo ou pronto para produção**.

---

# 3. Objetivo principal

O foco absoluto do projeto é praticar **TDD — Test-Driven Development**.

Portanto, novas funcionalidades devem ser desenvolvidas preferencialmente seguindo o ciclo:

1. RED
2. GREEN
3. REFACTOR

## RED

Criar primeiro um teste que descreva um comportamento ainda não implementado.

O teste deve falhar pelo motivo esperado.

## GREEN

Implementar somente o código mínimo necessário para fazer o teste passar.

Não antecipar funcionalidades futuras.

## REFACTOR

Após o teste passar:

- melhorar nomes;
- remover duplicações;
- reorganizar pequenas responsabilidades;
- simplificar estruturas;
- melhorar legibilidade;

sem alterar o comportamento externo protegido pelos testes.

Depois disso, iniciar um novo ciclo TDD.

---

# 4. Regra fundamental para agentes de IA

Uma IA **não deve implementar todo o sistema de uma vez**.

Ela deve respeitar o desenvolvimento incremental.

Quando solicitada a implementar uma funcionalidade usando TDD, deve preferir esta sequência:

```text
criar teste
    ↓
executar teste
    ↓
confirmar falha
    ↓
implementar mínimo necessário
    ↓
executar testes
    ↓
confirmar sucesso
    ↓
refatorar se necessário
```

A IA não deve criar antecipadamente dezenas de classes, interfaces, abstrações ou funcionalidades apenas porque poderão ser úteis no futuro.

O projeto deve seguir o princípio:

> Implementar somente o necessário para atender aos requisitos atuais.

---

# 5. Escopo técnico obrigatório

O projeto deve utilizar:

- Python;
- Pytest;
- objetos Python simples;
- `dataclasses` quando fizer sentido;
- listas em memória;
- `Enum` quando fizer sentido para representar tipos de serviço;
- `Decimal` para valores monetários.

Os dados devem existir apenas durante a execução do programa.

---

# 6. Tecnologias proibidas no escopo atual

Não adicionar sem autorização explícita do usuário:

- Django;
- Flask;
- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- MySQL;
- SQLite;
- MongoDB;
- Redis;
- qualquer banco de dados;
- API REST;
- GraphQL;
- interface gráfica;
- interface web;
- frontend;
- autenticação;
- autorização;
- Docker como requisito do sistema;
- microsserviços;
- filas;
- mensageria;
- ORM;
- persistência em arquivos;
- arquitetura distribuída;
- frameworks de injeção de dependência.

Também não adicionar infraestrutura de produção que não tenha relação direta com o aprendizado de TDD.

---

# 7. Arquitetura recomendada

Utilizar uma arquitetura simples em camadas, inspirada em conceitos de Clean Architecture, sem exagerar nas abstrações.

Estrutura recomendada:

```text
clinica-veterinaria/
│
├── pyproject.toml
├── README.md
├── agent.md
│
├── src/
│   └── clinica/
│       ├── __init__.py
│       │
│       ├── dominio/
│       │   ├── __init__.py
│       │   ├── animal.py
│       │   ├── responsavel.py
│       │   ├── atendimento.py
│       │   ├── servico.py
│       │   └── precificacao.py
│       │
│       ├── repositorios/
│       │   ├── __init__.py
│       │   ├── animal_repositorio.py
│       │   └── atendimento_repositorio.py
│       │
│       └── aplicacao/
│           ├── __init__.py
│           └── atendimento_service.py
│
└── tests/
    ├── dominio/
    │   ├── test_animal.py
    │   ├── test_atendimento.py
    │   └── test_precificacao.py
    │
    ├── repositorios/
    │   ├── test_animal_repositorio.py
    │   └── test_atendimento_repositorio.py
    │
    └── aplicacao/
        └── test_atendimento_service.py
```

A estrutura pode evoluir se houver necessidade real, mas deve permanecer simples.

---

# 8. Responsabilidades das camadas

## 8.1 Domínio

A camada de domínio contém:

- entidades;
- objetos de valor simples;
- regras de negócio;
- tipos de serviço;
- regras de precificação.

Possíveis classes:

- `Animal`;
- `Responsavel`;
- `Atendimento`;
- `TipoServico`;
- `CalculadoraAtendimento`.

A camada de domínio não deve depender de:

- banco de dados;
- framework web;
- interface gráfica;
- infraestrutura externa.

---

## 8.2 Repositórios

Os repositórios devem utilizar listas Python em memória.

Exemplos:

```python
self._animais = []
```

e:

```python
self._atendimentos = []
```

Possíveis classes:

- `AnimalRepositorio`;
- `AtendimentoRepositorio`.

Os repositórios são responsáveis por operações relacionadas às coleções de objetos.

Não criar persistência real.

---

## 8.3 Aplicação

A camada de aplicação deve coordenar casos de uso.

Exemplo:

`AtendimentoService`

Possíveis responsabilidades:

1. localizar o animal;
2. consultar atendimentos anteriores;
3. verificar regras de fidelidade;
4. calcular o valor;
5. criar o atendimento;
6. registrar o atendimento.

A camada de aplicação não deve conter detalhes de interface ou banco de dados.

---

# 9. Modelo de domínio inicial

## 9.1 Responsável

Representa a pessoa responsável por um animal.

Possíveis atributos iniciais:

- `id`;
- `nome`;
- `telefone`.

Não adicionar dezenas de dados pessoais sem necessidade.

---

## 9.2 Animal

Representa um animal cadastrado.

Possíveis atributos:

- `id`;
- `nome`;
- `especie`;
- `responsavel`.

O histórico de atendimentos pode ser mantido pelo repositório de atendimentos, em vez de necessariamente existir diretamente dentro de `Animal`.

A decisão deve priorizar simplicidade e testabilidade.

---

## 9.3 Atendimento

Representa um atendimento realizado.

Possíveis informações:

- animal;
- tipo de serviço;
- valor base;
- desconto;
- acréscimo;
- valor final.

Não transformar `Atendimento` em uma classe gigante.

---

## 9.4 TipoServico

Os serviços principais podem ser representados por `Enum`.

Valores básicos obrigatórios:

```text
Consulta de rotina       R$ 100,00
Consulta de urgência     R$ 180,00
Emergência               R$ 250,00
```

Exemplo possível:

```python
from decimal import Decimal
from enum import Enum


class TipoServico(Enum):
    ROTINA = Decimal("100.00")
    URGENCIA = Decimal("180.00")
    EMERGENCIA = Decimal("250.00")
```

A implementação pode ser ajustada se os testes demonstrarem uma alternativa mais adequada.

---

# 10. Valores monetários

Não utilizar `float` como representação principal de dinheiro.

Preferir:

```python
Decimal("100.00")
```

em vez de:

```python
100.00
```

Os cálculos devem evitar erros de precisão.

Sempre que possível, valores monetários devem retornar `Decimal`.

---

# 11. Regras de negócio obrigatórias

## 11.1 Consulta de rotina

Valor:

```text
R$ 100,00
```

---

## 11.2 Consulta de urgência

Valor:

```text
R$ 180,00
```

---

## 11.3 Atendimento de emergência

Valor:

```text
R$ 250,00
```

---

# 12. Regra de fidelidade

Um animal recebe desconto de fidelidade de:

```text
10%
```

quando possuir pelo menos:

```text
5 atendimentos anteriores
```

A palavra **anteriores** é importante.

Portanto:

```text
1º atendimento → sem desconto
2º atendimento → sem desconto
3º atendimento → sem desconto
4º atendimento → sem desconto
5º atendimento → sem desconto
6º atendimento → desconto de fidelidade
```

O sexto atendimento é o primeiro que possui cinco atendimentos anteriores.

A IA não deve reinterpretar automaticamente a regra para aplicar desconto no quinto atendimento.

---

# 13. Exemplos esperados de fidelidade

Consulta de rotina com fidelidade:

```text
Valor original = R$ 100,00
Desconto       = 10%
Valor final    = R$ 90,00
```

Consulta de urgência com fidelidade:

```text
Valor original = R$ 180,00
Desconto       = 10%
Valor final    = R$ 162,00
```

Emergência com fidelidade:

```text
Valor original = R$ 250,00
Desconto       = 10%
Valor final    = R$ 225,00
```

---

# 14. Acréscimos

O sistema pode permitir procedimentos adicionais ou acréscimos.

Porém:

- não inventar tipos de procedimentos sem requisito;
- não inventar percentuais;
- não inventar preços;
- não implementar regras adicionais apenas por previsão futura.

Quando houver um procedimento adicional explicitamente definido, o cálculo correspondente deve ser coberto por testes.

---

# 15. Ordem entre desconto e acréscimo

A ordem de aplicação de desconto e acréscimo **não deve ser inventada pela IA**.

Por exemplo:

```text
Consulta = R$ 100
Procedimento adicional = R$ 50
Fidelidade = 10%
```

Existem pelo menos duas interpretações possíveis:

```text
desconto sobre R$ 100
```

ou:

```text
desconto sobre R$ 150
```

Se o requisito ainda não definir isso, a IA deve:

1. não assumir silenciosamente uma regra;
2. deixar a decisão explícita antes de consolidar a implementação;
3. proteger a regra escolhida através de teste.

---

# 16. Valores inválidos

O sistema deve proteger suas regras contra valores monetários inválidos quando esses valores puderem ser informados manualmente.

Casos relevantes:

- valor zero quando não permitido;
- valor negativo;
- desconto negativo;
- acréscimo negativo;
- valor final negativo.

Não adicionar validações arbitrárias que não estejam relacionadas ao domínio do projeto.

---

# 17. Operações obrigatórias sobre animais

O sistema deve praticar manipulação de listas.

As operações previstas incluem:

- adicionar;
- listar;
- buscar;
- filtrar;
- ordenar;
- remover.

Possíveis métodos:

```text
adicionar()
listar()
buscar_por_id()
buscar_por_nome()
filtrar_por_especie()
ordenar_por_nome()
remover()
```

A implementação pode variar, desde que mantenha simplicidade e seja protegida por testes.

---

# 18. Operações sobre atendimentos

Possíveis operações:

```text
adicionar()
listar()
buscar_por_animal()
contar_por_animal()
total_gasto_por_animal()
```

O sistema deve conseguir responder:

- quantos atendimentos determinado animal realizou;
- quais são seus atendimentos;
- quanto ele gastou;
- se já possui fidelidade.

---

# 19. Total gasto

Para um animal com atendimentos:

```text
Rotina       = R$ 100,00
Urgência     = R$ 180,00
Emergência   = R$ 250,00
```

o total esperado é:

```text
R$ 530,00
```

Um animal sem atendimentos deve possuir total:

```text
R$ 0,00
```

Preferencialmente:

```python
Decimal("0.00")
```

e não `None`.

---

# 20. Comportamento para animal inexistente

Quando uma operação exigir que o animal exista, o comportamento deve ser definido claramente.

Exemplo de requisito existente:

```python
test_animal_inexistente_lanca_excecao()
```

Portanto, nos casos em que esse teste representar o comportamento oficial do sistema, a implementação deve lançar uma exceção apropriada.

Não misturar comportamentos inconsistentes como:

- em um método lançar exceção;
- em outro retornar `None`;
- em outro retornar `False`;

sem um motivo claro.

---

# 21. Testes devem verificar comportamento

Evitar testes focados apenas na implementação interna.

Preferir:

```python
def test_sexto_atendimento_recebe_desconto_fidelidade():
    ...
```

em vez de:

```python
def test_metodo_calcular():
    ...
```

Os testes devem funcionar como documentação executável das regras.

---

# 22. Padrão para nomes dos testes

Preferir nomes descritivos.

Exemplos:

```python
test_calcular_valor_consulta_rotina()
test_calcular_valor_consulta_urgencia()
test_calcular_valor_atendimento_emergencia()
test_animal_sem_atendimentos_deve_ter_total_zero()
test_quinto_atendimento_nao_recebe_desconto()
test_sexto_atendimento_recebe_desconto_fidelidade()
```

Evitar nomes genéricos como:

```python
test_1()
test_funcao()
test_calculo()
```

---

# 23. Testes iniciais obrigatórios

Os seguintes testes fazem parte da proposta original do projeto.

## Serviços e valores

```python
test_calcular_valor_consulta_rotina()
test_calcular_valor_consulta_urgencia()
test_calcular_valor_atendimento_emergencia()
```

## Acúmulo e total

```python
test_acumular_valores_varios_atendimentos()
test_consultar_total_gasto_animal_existente()
```

## Fidelidade

```python
test_aplicar_desconto_fidelidade()
test_nao_aplicar_desconto_sem_fidelidade()
test_calcular_atendimento_com_desconto()
```

## Validações

```python
test_nao_permitir_valor_servico_zero()
test_calcular_valores_decimais()
test_nao_permitir_valor_negativo()
test_animal_inexistente_lanca_excecao()
```

## Cadastro

```python
test_registrar_novo_animal_sem_atendimentos()
```

## Acréscimos

```python
test_aplicar_acrescimo_procedimento_adicional()
```

## Regras futuras

```python
test_identificar_retorno_dentro_do_periodo()
```

Essa regra ainda precisa de uma definição funcional precisa antes de ser implementada.

## Listas

```python
test_registrar_varios_animais_em_lista()
test_calcular_total_gasto_lista_animais()
test_filtrar_animais_com_gasto_acima_de_limite()
test_ordenar_animais_por_total_gasto()
test_remover_animais_sem_atendimentos()
test_buscar_animal_por_nome()
test_somar_faturamento_total_lista()
test_ranking_animais_por_total_gasto()
```

---

# 24. Testes adicionais recomendados

Além dos testes originais, são recomendados:

## Serviço

```python
test_tipo_servico_invalido_lanca_excecao()
test_valor_servico_deve_ser_decimal()
test_nao_permitir_valor_servico_negativo()
```

## Animal e responsável

```python
test_animal_deve_possuir_responsavel()
test_animal_deve_iniciar_sem_atendimentos()
test_nao_permitir_nome_animal_vazio()
test_nao_permitir_nome_responsavel_vazio()
test_animal_deve_possuir_identificador()
```

Só implementar validações que sejam assumidas como regra oficial do projeto.

## Registro de atendimento

```python
test_registrar_atendimento_para_animal()
test_animal_deve_possuir_um_atendimento_apos_registro()
test_registrar_multiplos_atendimentos_para_mesmo_animal()
```

## Total gasto

```python
test_animal_sem_atendimentos_deve_ter_total_zero()
test_total_gasto_deve_considerar_todos_atendimentos()
```

## Fidelidade

```python
test_primeiro_atendimento_nao_recebe_desconto()
test_quarto_atendimento_nao_recebe_desconto()
test_quinto_atendimento_nao_recebe_desconto()
test_sexto_atendimento_recebe_desconto_fidelidade()
test_desconto_fidelidade_deve_ser_de_dez_porcento()
test_urgencia_com_fidelidade_deve_custar_162()
test_emergencia_com_fidelidade_deve_custar_225()
```

## Acréscimos

```python
test_atendimento_sem_adicional_nao_deve_ter_acrescimo()
test_multiplos_acrescimos_devem_ser_somados()
test_calcular_atendimento_com_desconto_e_acrescimo()
```

## Proteções matemáticas

```python
test_desconto_nao_pode_superar_valor_atendimento()
test_valor_final_deve_possuir_duas_casas_decimais()
test_acrescimo_negativo_deve_ser_rejeitado()
test_desconto_negativo_deve_ser_rejeitado()
```

## Listas e repositórios

```python
test_lista_animais_deve_iniciar_vazia()
test_adicionar_animal_na_lista()
test_buscar_animal_por_id()
test_buscar_animal_inexistente_retorna_none()
test_nao_permitir_animais_com_mesmo_id()
```

A forma de tratar busca inexistente deve permanecer consistente com as regras oficiais adotadas no projeto.

## Filtros

```python
test_filtrar_animais_por_especie()
test_filtro_sem_resultados_retorna_lista_vazia()
test_filtrar_animais_com_gasto_acima_de_limite()
```

## Ordenação

```python
test_ordenar_animais_por_nome()
test_ordenar_animais_por_total_gasto()
test_ordenar_por_total_gasto_nao_altera_valores()
```

## Operações coletivas

```python
test_calcular_total_gasto_lista_animais()
test_somar_faturamento_total_lista()
test_faturamento_lista_vazia_deve_ser_zero()
```

## Ranking

```python
test_ranking_animais_por_total_gasto()
test_ranking_deve_ser_decrescente()
test_ranking_com_animais_sem_atendimentos()
test_ranking_lista_vazia()
```

---

# 25. Ordem recomendada de desenvolvimento

A IA deve preferir esta sequência para manter o aprendizado gradual.

## Etapa 1 — Serviços básicos

Implementar através de TDD:

```python
test_calcular_valor_consulta_rotina()
test_calcular_valor_consulta_urgencia()
test_calcular_valor_atendimento_emergencia()
test_calcular_valores_decimais()
```

Depois tratar entradas inválidas relacionadas aos serviços.

---

## Etapa 2 — Responsável e Animal

Criar os modelos mínimos necessários.

Testes sugeridos:

```python
test_registrar_novo_animal_sem_atendimentos()
test_animal_deve_possuir_responsavel()
test_animal_deve_iniciar_sem_atendimentos()
```

Não adicionar atributos desnecessários.

---

## Etapa 3 — Registro de atendimentos

Testes:

```python
test_registrar_atendimento_para_animal()
test_animal_deve_possuir_um_atendimento_apos_registro()
test_registrar_multiplos_atendimentos_para_mesmo_animal()
test_acumular_valores_varios_atendimentos()
```

---

## Etapa 4 — Total gasto

Testes:

```python
test_consultar_total_gasto_animal_existente()
test_animal_sem_atendimentos_deve_ter_total_zero()
test_total_gasto_deve_considerar_todos_atendimentos()
test_animal_inexistente_lanca_excecao()
```

---

## Etapa 5 — Fidelidade

Desenvolver gradualmente.

Testes:

```python
test_primeiro_atendimento_nao_recebe_desconto()
test_quinto_atendimento_nao_recebe_desconto()
test_sexto_atendimento_recebe_desconto_fidelidade()
test_aplicar_desconto_fidelidade()
test_calcular_atendimento_com_desconto()
test_urgencia_com_fidelidade_deve_custar_162()
test_emergencia_com_fidelidade_deve_custar_225()
```

---

## Etapa 6 — Acréscimos

Testes:

```python
test_aplicar_acrescimo_procedimento_adicional()
test_atendimento_sem_adicional_nao_deve_ter_acrescimo()
test_multiplos_acrescimos_devem_ser_somados()
```

Só depois adicionar combinações como:

```python
test_calcular_atendimento_com_desconto_e_acrescimo()
```

---

## Etapa 7 — Validações

Testes de borda:

```python
test_nao_permitir_valor_servico_zero()
test_nao_permitir_valor_negativo()
test_acrescimo_negativo_deve_ser_rejeitado()
test_desconto_negativo_deve_ser_rejeitado()
```

---

## Etapa 8 — Repositório de animais

Começar pelas operações simples.

```python
test_lista_animais_deve_iniciar_vazia()
test_adicionar_animal_na_lista()
test_registrar_varios_animais_em_lista()
test_buscar_animal_por_nome()
test_buscar_animal_por_id()
test_remover_animal_da_lista()
```

---

## Etapa 9 — Filtros

```python
test_filtrar_animais_por_especie()
test_filtro_sem_resultados_retorna_lista_vazia()
test_filtrar_animais_com_gasto_acima_de_limite()
```

---

## Etapa 10 — Ordenação

```python
test_ordenar_animais_por_nome()
test_ordenar_animais_por_total_gasto()
```

---

## Etapa 11 — Cálculos coletivos

```python
test_calcular_total_gasto_lista_animais()
test_somar_faturamento_total_lista()
test_faturamento_lista_vazia_deve_ser_zero()
```

---

## Etapa 12 — Ranking

```python
test_ranking_animais_por_total_gasto()
test_ranking_deve_ser_decrescente()
test_ranking_com_animais_sem_atendimentos()
test_ranking_lista_vazia()
```

---

## Etapa 13 — Remoções condicionais

Somente após o funcionamento das operações básicas.

```python
test_remover_animais_sem_atendimentos()
```

Não inventar automaticamente a regra:

```python
test_nao_remover_animal_com_atendimentos()
```

Ela só deve ser implementada se for adotada explicitamente como requisito.

---

## Etapa 14 — Regras futuras

Somente após o núcleo estar estável.

Exemplo:

```python
test_identificar_retorno_dentro_do_periodo()
```

Essa funcionalidade depende de requisitos ainda não definidos.

---

# 26. Regra de retorno ainda NÃO definida

Não assumir automaticamente que retorno:

- ocorre em 7 dias;
- ocorre em 15 dias;
- ocorre em 30 dias;
- é gratuito;
- possui desconto;
- só vale para rotina;
- vale para urgência;
- vale para emergência.

Antes de implementar essa funcionalidade deve existir uma regra explícita.

Exemplo de possível regra futura:

```text
Um retorno realizado até 15 dias após uma consulta de rotina não gera nova cobrança.
```

Somente após uma definição semelhante devem existir testes como:

```python
test_retorno_dentro_de_15_dias_nao_deve_ser_cobrado()
test_retorno_com_exatos_15_dias_deve_ser_gratuito()
test_retorno_apos_15_dias_deve_ser_cobrado()
test_retorno_deve_pertencer_ao_mesmo_animal()
```

---

# 27. Não inventar requisitos

Uma IA trabalhando neste projeto não deve transformar sugestões em requisitos oficiais.

Exemplos de regras que **não são obrigatórias**, a menos que sejam explicitamente solicitadas:

- desconto para animais idosos;
- desconto por espécie;
- cobrança noturna;
- desconto progressivo de 15%;
- limite máximo de 25% de desconto;
- retorno gratuito;
- bloqueio de remoção de animal com histórico;
- controle de vacinas;
- prontuário;
- consultas agendadas;
- veterinários;
- pagamentos;
- estoque;
- medicamentos.

Essas ideias podem ser sugeridas, mas não implementadas silenciosamente.

---

# 28. Não antecipar generalizações

Evitar criar estruturas como:

```text
AbstractService
AbstractRepository
BaseEntity
BaseCalculator
RuleEngine
PricingStrategyFactory
DependencyInjectionContainer
```

se ainda não houver necessidade real.

Este projeto é didático.

Preferir código simples e explícito.

---

# 29. Uso de padrões de projeto

Padrões podem ser utilizados quando resolverem um problema existente.

O projeto pode naturalmente utilizar conceitos como:

- Repository Pattern;
- Service Layer;
- Domain Model.

Porém, uma IA não deve adicionar padrões apenas para tornar a arquitetura aparentemente mais sofisticada.

---

# 30. Mocks

Evitar o uso excessivo de mocks.

Os repositórios são baseados em listas em memória e são rápidos.

Portanto, preferir:

```python
repo = AtendimentoRepositorio()
```

a:

```python
repo = MagicMock()
```

quando o objeto real for simples e determinístico.

Mocks poderão ser utilizados futuramente se surgirem dependências externas reais.

---

# 31. Fixtures do Pytest

Fixtures podem ser utilizadas para reduzir repetição.

Porém:

- não esconder demais a preparação dos testes;
- manter os cenários compreensíveis;
- evitar fixtures gigantes;
- preferir fixtures pequenas e reutilizáveis.

Um teste deve continuar legível sem exigir navegação por muitos arquivos.

---

# 32. Parametrize

`pytest.mark.parametrize` pode ser utilizado quando vários cenários tiverem a mesma estrutura.

Exemplo adequado:

```python
@pytest.mark.parametrize(
    "tipo, valor_esperado",
    [
        (TipoServico.ROTINA, Decimal("100.00")),
        (TipoServico.URGENCIA, Decimal("180.00")),
        (TipoServico.EMERGENCIA, Decimal("250.00")),
    ],
)
def test_valor_servico(tipo, valor_esperado):
    assert tipo.value == valor_esperado
```

Entretanto, durante as primeiras etapas de aprendizado de TDD, testes separados podem ser mantidos se ajudarem a compreender melhor cada comportamento.

---

# 33. Testes independentes

Cada teste deve poder rodar isoladamente.

Não criar dependência como:

```text
teste A precisa rodar antes de teste B
```

Cada teste deve preparar seu próprio estado.

---

# 34. Estado compartilhado

Evitar variáveis globais mutáveis.

Cada repositório utilizado em um teste deve preferencialmente começar em estado controlado.

---

# 35. Testes determinísticos

Os testes não devem depender de:

- internet;
- horário do computador;
- banco externo;
- API;
- arquivos externos;
- ordem de execução;
- valores aleatórios sem controle.

Se uma regra futura utilizar data e hora, tornar essa dependência testável.

---

# 36. Cobertura

Pode ser utilizado:

```bash
pytest --cov=src
```

ou:

```bash
pytest --cov=src --cov-report=term-missing
```

Porém:

> 100% de cobertura não é o objetivo principal.

Não criar testes sem valor apenas para aumentar a porcentagem.

Priorizar cobertura das regras de negócio e comportamentos relevantes.

---

# 37. Prioridade dos testes

Priorizar:

1. regras de negócio;
2. casos de borda;
3. comportamento em entradas inválidas;
4. interações entre regras;
5. regressões;
6. operações sobre listas.

Evitar gastar tempo testando detalhes triviais da própria linguagem Python.

---

# 38. Refatoração

Refatorações devem preservar os testes existentes.

Antes de refatorar:

```bash
pytest
```

Após refatorar:

```bash
pytest
```

Todos os testes previamente válidos devem continuar passando.

---

# 39. Alteração de comportamento

Se uma refatoração alterar o comportamento observável do sistema, ela deixou de ser apenas uma refatoração.

Nesse caso:

1. criar ou alterar o teste correspondente;
2. justificar a mudança com base em requisito;
3. implementar a nova regra.

---

# 40. Falhas de testes

Uma IA não deve fazer um teste passar simplesmente:

- removendo o teste;
- comentando o teste;
- enfraquecendo uma asserção;
- capturando exceções indevidamente;
- adicionando condições especiais apenas para o teste;
- retornando valores hard-coded sem representar a regra.

A implementação deve atender ao comportamento.

---

# 41. Não alterar testes para acomodar código incorreto

Quando um teste estiver correto segundo o requisito e a implementação falhar, corrigir a implementação.

Não modificar o teste apenas para aceitar um comportamento errado.

---

# 42. Quando alterar um teste

Um teste pode ser alterado quando:

- o requisito mudou;
- o teste estava objetivamente incorreto;
- o teste estava testando implementação em vez de comportamento;
- ocorreu uma refatoração legítima da estrutura dos testes sem mudar a regra.

---

# 43. Simplicidade acima de abstração

Preferir:

```python
def total_gasto_por_animal(...):
    ...
```

a criar uma cadeia complexa de abstrações se uma função ou classe simples resolver corretamente o problema.

---

# 44. Legibilidade

O código deve priorizar:

- nomes claros;
- funções pequenas;
- responsabilidades claras;
- ausência de duplicação desnecessária;
- fluxo fácil de entender.

A meta não é escrever o menor número possível de linhas.

A meta é criar código claro para quem está aprendendo.

---

# 45. Idioma

Os nomes podem permanecer em português para acompanhar o domínio e os testes já definidos.

Exemplos:

```python
Animal
Responsavel
Atendimento
TipoServico
AnimalRepositorio
AtendimentoRepositorio
AtendimentoService
```

Evitar misturar português e inglês sem necessidade.

---

# 46. Exceções

Quando uma regra exigir erro de domínio, preferir exceções claras.

Exemplos possíveis:

```python
AnimalNaoEncontradoError
ValorServicoInvalidoError
```

Porém, não criar uma hierarquia complexa de exceções sem necessidade.

---

# 47. Futuras evoluções

Novos requisitos podem ser adicionados para continuar praticando TDD.

Exemplos possíveis:

- desconto para animais idosos;
- acréscimo noturno;
- diferentes níveis de fidelidade;
- limite máximo de desconto;
- retorno gratuito dentro de um período.

Cada evolução deve começar por testes.

---

# 48. Checklist antes de implementar uma nova funcionalidade

Uma IA deve verificar:

- [ ] Existe requisito explícito para essa funcionalidade?
- [ ] O comportamento está claro?
- [ ] Existe alguma ambiguidade?
- [ ] O teste pode ser escrito antes da implementação?
- [ ] Estou implementando somente o necessário?
- [ ] Estou evitando dependências externas?
- [ ] O código continuará simples?
- [ ] Estou preservando as regras existentes?

---

# 49. Checklist RED

Antes da implementação:

- [ ] Criar teste.
- [ ] Executar teste.
- [ ] Confirmar que falha.
- [ ] Confirmar que falha pelo motivo esperado.

Um teste que já nasce passando pode indicar que:

- o comportamento já existe;
- o teste está incorreto;
- o teste não está verificando o comportamento pretendido.

---

# 50. Checklist GREEN

Durante a implementação:

- [ ] Escrever apenas o mínimo necessário.
- [ ] Não antecipar funcionalidades.
- [ ] Executar o teste.
- [ ] Executar também os testes anteriores.
- [ ] Confirmar ausência de regressões.

---

# 51. Checklist REFACTOR

Após os testes passarem:

- [ ] Há duplicação evidente?
- [ ] Os nomes estão claros?
- [ ] Alguma função possui responsabilidade excessiva?
- [ ] A solução pode ficar mais simples?
- [ ] Os testes continuam legíveis?
- [ ] Todos os testes continuam passando?

---

# 52. O que uma IA NÃO deve fazer

É proibido fugir da proposta adicionando por iniciativa própria:

```text
API
frontend
banco de dados
Docker
autenticação
deploy
microsserviços
ORM
painel administrativo
framework web
persistência
arquiteturas excessivamente complexas
```

Também não deve:

- escrever todos os testes de uma vez quando o objetivo da tarefa for praticar TDD passo a passo;
- implementar todos os requisitos futuros antecipadamente;
- criar código genérico sem necessidade;
- substituir `Decimal` por `float` sem justificativa;
- ignorar a regra dos cinco atendimentos anteriores;
- alterar regras de negócio sem autorização;
- criar funcionalidades que não foram solicitadas;
- transformar o projeto didático em um produto de produção.

---

# 53. O que uma IA DEVE fazer

Uma IA deve:

- preservar o foco em TDD;
- escrever código simples;
- explicar decisões importantes;
- implementar de maneira incremental;
- proteger regras com testes;
- executar a suíte após alterações;
- manter as camadas separadas;
- usar listas em memória;
- usar `Decimal` para dinheiro;
- manter o código apropriado para aprendizado;
- apontar ambiguidades de requisito antes de consolidar regras inventadas.

---

# 54. Critério de conclusão do projeto

O projeto pode ser considerado funcional quando:

- os três serviços básicos estiverem implementados;
- animais puderem ser registrados;
- responsáveis puderem ser associados aos animais;
- atendimentos puderem ser registrados;
- valores puderem ser calculados;
- histórico puder ser consultado;
- total gasto puder ser calculado;
- fidelidade funcionar corretamente;
- acréscimos definidos puderem ser aplicados;
- listas de animais puderem ser manipuladas;
- busca funcionar;
- filtros funcionarem;
- ordenação funcionar;
- remoção prevista funcionar;
- faturamento total puder ser calculado;
- ranking puder ser gerado;
- regras de negócio estiverem cobertas por testes relevantes.

---

# 55. Princípio final

Este projeto deve permanecer:

```text
pequeno
+
simples
+
testável
+
incremental
+
orientado a regras de negócio
+
orientado por testes
```

A finalidade principal não é construir rapidamente um sistema veterinário completo.

A finalidade é aprender a desenvolver software de forma incremental utilizando:

```text
Python
+
Pytest
+
TDD
+
Orientação a Objetos
+
Regras de Negócio
+
Refatoração
```

Qualquer IA que trabalhe neste projeto deve preservar essa finalidade.