# Clínica Veterinária — Projeto de TDD com Python e Pytest

Projeto simples de gerenciamento de atendimentos de uma clínica veterinária, desenvolvido com foco no aprendizado de **TDD (Test-Driven Development)** utilizando **Python** e **Pytest**.

A proposta é praticar testes unitários e implementação de regras de negócio sem utilizar banco de dados, interface gráfica ou frameworks web. Todos os dados são manipulados em memória através de listas e objetos simples.

## Objetivo

O principal objetivo deste projeto é praticar o desenvolvimento orientado a testes, criando os testes antes da implementação das funcionalidades.


## Contexto do sistema

Uma clínica veterinária precisa de um sistema simples para registrar animais, seus responsáveis e os atendimentos realizados.

Cada atendimento possui um serviço principal e um valor correspondente. Algumas regras podem modificar o preço final, como descontos de fidelidade e futuros acréscimos.

O sistema foi propositalmente mantido pequeno para que o foco permaneça na lógica de negócio e nos testes automatizados.

## Regras de negócio

Inicialmente, o sistema possui três tipos de atendimento:

| Serviço                   |     Valor |
| ------------------------- | --------: |
| Consulta de rotina        | R$ 100,00 |
| Consulta de urgência      | R$ 180,00 |
| Atendimento de emergência | R$ 250,00 |

### Desconto de fidelidade

Um animal recebe **10% de desconto** quando possuir pelo menos **5 atendimentos anteriores**.

Isso significa que o desconto começa a ser aplicado a partir do sexto atendimento.

Exemplo:

```text
1º atendimento → sem desconto
2º atendimento → sem desconto
3º atendimento → sem desconto
4º atendimento → sem desconto
5º atendimento → sem desconto
6º atendimento → desconto de 10%
```

## Funcionalidades

O sistema deverá permitir:

* cadastrar animais;
* cadastrar responsáveis;
* registrar atendimentos;
* calcular o valor de um atendimento;
* consultar os atendimentos de um animal;
* consultar o total gasto por um animal;
* contar a quantidade de atendimentos anteriores;
* aplicar desconto de fidelidade;
* adicionar animais em memória;
* buscar animais;
* filtrar animais;
* ordenar animais;
* remover animais.

## Tecnologias utilizadas

* Python
* Pytest
* Pytest-Cov
* `dataclasses`
* `enum`
* `decimal.Decimal`

Não serão utilizados:

* banco de dados;
* interface gráfica;
* APIs REST;
* Django;
* Flask;
* FastAPI;
* SQLAlchemy.

O objetivo é manter o projeto simples e focado em testes e regras de negócio.

## Demonstração manual

O projeto inclui uma demonstração visual no terminal. Ela cadastra animais e
responsáveis, registra atendimentos, aplica fidelidade, acréscimo e retorno
gratuito, e mostra buscas, filtros, ordenações, ranking, remoção e faturamento.

Na raiz do projeto, execute:

```powershell
.\.venv\Scripts\Activate.ps1
python demo_manual.py
```

A demonstração usa somente dados em memória e verifica os resultados com
asserções antes de apresentar a mensagem de sucesso.

## Arquitetura

O projeto utiliza uma arquitetura em camadas simplificada, inspirada em conceitos de Clean Architecture.

A divisão principal é:

```text
Domínio
    ↓
Aplicação / Serviços
    ↓
Repositórios em memória
```

### Domínio

Contém as principais entidades e regras do sistema.

Exemplos:

```text
Animal
Responsavel
Atendimento
TipoServico
CalculadoraAtendimento
```


## Desenvolvimento utilizando TDD

O projeto deverá ser desenvolvido seguindo o ciclo:

```text
RED
 ↓
GREEN
 ↓
REFACTOR
```

### RED

Criar um teste para uma funcionalidade que ainda não existe.

O teste deverá falhar.

### GREEN

Implementar apenas o código necessário para fazer o teste passar.

### REFACTOR

Melhorar o código mantendo todos os testes funcionando.

Depois disso, o ciclo é iniciado novamente para a próxima regra.

```text
Teste
  ↓
Falha
  ↓
Implementação mínima
  ↓
Teste passa
  ↓
Refatoração
  ↓
Próximo teste
```


## Conclusão

Este projeto foi criado como ambiente de aprendizado para compreender na prática como testes automatizados podem orientar o desenvolvimento de software.

Ao invés de implementar todo o sistema primeiro e escrever testes posteriormente, cada funcionalidade deverá nascer a partir de um teste.

Essa abordagem permite praticar:

* definição clara dos requisitos;
* criação de código testável;
* detecção rápida de regressões;
* evolução segura das regras;
* refatoração contínua;
* desenvolvimento incremental.

O principal objetivo não é terminar o sistema rapidamente, mas compreender o processo de construção de software orientado por testes.
