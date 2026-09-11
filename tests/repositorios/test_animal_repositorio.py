from uuid import uuid4
import pytest
from decimal import Decimal

from clinica.aplicacao.atendimento_service import registrar_atendimento
from clinica.dominio.animal import Animal
from clinica.dominio.atendimento import Atendimento
from clinica.dominio.responsavel import Responsavel
from clinica.repositorios.animal_repositorio import AnimalRepositorio

def criar_animal(nome: str) -> Animal:
    responsavel = Responsavel(nome="Maria")

    return Animal(
        nome=nome,
        responsavel=responsavel,
    )

def test_registrar_novo_animal_sem_atendimentos():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Rex", responsavel=responsavel)

    repositorio.adicionar(animal)

    animal_encontrado = repositorio.buscar_por_id(animal.id)

    assert animal_encontrado == animal
    assert animal_encontrado.atendimentos == []


def test_lista_animais_deve_iniciar_vazia():
    repositorio = AnimalRepositorio()

    animais = repositorio.listar()

    assert animais == []

def test_adicionar_animal_na_lista():
    repositorio = AnimalRepositorio()
    animal = criar_animal("Rex")

    repositorio.adicionar(animal)

    assert repositorio.listar() == [animal] 

def test_registrar_varios_animais_em_lista():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")
    bidu = criar_animal("Bidu")

    repositorio.adicionar(rex)
    repositorio.adicionar(mia)
    repositorio.adicionar(bidu)

    assert repositorio.listar() == [rex, mia, bidu]

def test_buscar_animal_por_nome():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")
    repositorio.adicionar(rex)
    repositorio.adicionar(mia)

    animal_encontrado = repositorio.buscar_por_nome("Mia")

    assert animal_encontrado is mia

def test_remover_animal_da_lista():
    repositorio = AnimalRepositorio()
    animal = criar_animal("Rex")
    repositorio.adicionar(animal)

    repositorio.remover(animal.id)

    assert repositorio.listar() == []
    assert repositorio.buscar_por_id(animal.id) is None

def test_buscar_animal_por_id():
    repositorio = AnimalRepositorio()
    animal = criar_animal("Rex")
    repositorio.adicionar(animal)

    animal_encontrado = repositorio.buscar_por_id(animal.id)

    assert animal_encontrado is animal

def test_buscar_animal_inexistente_retorna_none():
    repositorio = AnimalRepositorio()

    animal_encontrado = repositorio.buscar_por_id(uuid4())

    assert animal_encontrado is None


def test_nao_permitir_animais_com_mesmo_id():
    repositorio = AnimalRepositorio()
    primeiro_animal = criar_animal("Rex")
    segundo_animal = criar_animal("Mia")
    segundo_animal.id = primeiro_animal.id

    repositorio.adicionar(primeiro_animal)

    with pytest.raises(
        ValueError,
        match="Animal com este identificador já cadastrado",
    ):
        repositorio.adicionar(segundo_animal)

    assert repositorio.listar() == [primeiro_animal] 

def test_remover_animais_sem_atendimentos():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal_com_atendimento = Animal(nome="Rex", responsavel=responsavel)
    animal_sem_atendimento = Animal(nome="Mia", responsavel=responsavel)

    animal_com_atendimento.adicionar_atendimento(
        Atendimento(tipo_servico="consulta_rotina", valor=Decimal("100.00")),
    )

    repositorio.adicionar(animal_com_atendimento)
    repositorio.adicionar(animal_sem_atendimento)

    repositorio.remover_animais_sem_atendimentos()

    assert repositorio.listar() == [animal_com_atendimento]
    assert repositorio.buscar_por_id(animal_sem_atendimento.id) is None


def test_nao_remover_animal_com_atendimentos():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Rex", responsavel=responsavel)

    animal.adicionar_atendimento(
        Atendimento(tipo_servico="consulta_urgencia", valor=Decimal("180.00")),
    )

    repositorio.adicionar(animal)

    repositorio.remover_animais_sem_atendimentos()

    assert repositorio.listar() == [animal]
    assert repositorio.buscar_por_id(animal.id) == animal

def criar_repositorio_com_especies():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")

    rex = Animal(nome="Rex", especie="cachorro", responsavel=responsavel)
    mia = Animal(nome="Mia", especie="gato", responsavel=responsavel)
    bob = Animal(nome="Bob", especie="cachorro", responsavel=responsavel)

    for animal in (rex, mia, bob):
        repositorio.adicionar(animal)

    return repositorio, rex, mia, bob


def test_filtrar_animais_por_especie():
    repositorio, rex, mia, bob = criar_repositorio_com_especies()

    cachorros = repositorio.filtrar_por_especie("cachorro")

    assert cachorros == [rex, bob]
    assert mia not in cachorros
    assert repositorio.filtrar_por_especie("gato") == [mia]


def test_filtro_sem_resultados_retorna_lista_vazia():
    repositorio, _, _, _ = criar_repositorio_com_especies()

    assert repositorio.filtrar_por_especie("coelho") == []
    assert repositorio.filtrar_por_gasto_acima_de(Decimal("1000.00")) == []

    repositorio_vazio = AnimalRepositorio()

    assert repositorio_vazio.filtrar_por_especie("cachorro") == []


def test_filtrar_animais_com_gasto_acima_de_limite():
    repositorio, rex, mia, bob = criar_repositorio_com_especies()

    registrar_atendimento(rex, "consulta_emergencia")
    registrar_atendimento(mia, "consulta_rotina")

    assert rex.total_gasto() == Decimal("250.00")
    assert mia.total_gasto() == Decimal("100.00")
    assert bob.total_gasto() == Decimal("0.00")

    assert repositorio.filtrar_por_gasto_acima_de(Decimal("150.00")) == [rex]
    assert repositorio.filtrar_por_gasto_acima_de(Decimal("50.00")) == [rex, mia]

    # "acima de" e estritamente maior: o valor exato do limite fica de fora.
    assert repositorio.filtrar_por_gasto_acima_de(Decimal("250.00")) == []
    assert repositorio.filtrar_por_gasto_acima_de(Decimal("0.00")) == [rex, mia]
def test_ordenar_animais_por_nome():
    repositorio = AnimalRepositorio()
    zeca = criar_animal("Zeca")
    bidu = criar_animal("Bidu")
    amora = criar_animal("Amora")

    repositorio.adicionar(zeca)
    repositorio.adicionar(bidu)
    repositorio.adicionar(amora)

    repositorio.ordenar_por_nome()

    assert repositorio.listar() == [amora, bidu, zeca]

def test_ordenar_animais_por_total_gasto():
    repositorio = AnimalRepositorio()
    animal_urgencia = criar_animal("Rex")
    animal_sem_atendimento = criar_animal("Mia")
    animal_rotina = criar_animal("Bidu")

    animal_urgencia.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_urgencia",
            valor=Decimal("180.00"),
        )
    )
    animal_rotina.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_rotina",
            valor=Decimal("100.00"),
        )
    )

    repositorio.adicionar(animal_urgencia)
    repositorio.adicionar(animal_sem_atendimento)
    repositorio.adicionar(animal_rotina)

    repositorio.ordenar_por_total_gasto()

    assert repositorio.listar() == [
        animal_sem_atendimento,
        animal_rotina,
        animal_urgencia,
    ]

def test_ordenar_por_total_gasto_nao_altera_valores():
    repositorio = AnimalRepositorio()
    animal_rotina = criar_animal("Rex")
    animal_urgencia = criar_animal("Mia")

    animal_rotina.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_rotina",
            valor=Decimal("100.00"),
        )
    )
    animal_urgencia.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_urgencia",
            valor=Decimal("180.00"),
        )
    )

    repositorio.adicionar(animal_urgencia)
    repositorio.adicionar(animal_rotina)

    repositorio.ordenar_por_total_gasto()

    assert animal_rotina.total_gasto() == Decimal("100.00")
    assert animal_urgencia.total_gasto() == Decimal("180.00")
    assert animal_rotina.atendimentos[0].valor == Decimal("100.00")
    assert animal_urgencia.atendimentos[0].valor == Decimal("180.00")


def test_ranking_animais_por_total_gasto():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")
    bidu = criar_animal("Bidu")

    registrar_atendimento(rex, "consulta_rotina")
    registrar_atendimento(mia, "consulta_emergencia")
    registrar_atendimento(bidu, "consulta_urgencia")

    repositorio.adicionar(rex)
    repositorio.adicionar(mia)
    repositorio.adicionar(bidu)

    ranking = repositorio.ranking_por_total_gasto()

    assert ranking == [mia, bidu, rex]

    # O ranking e uma consulta: nao altera a ordem interna do repositorio.
    assert repositorio.listar() == [rex, mia, bidu]


def test_ranking_deve_ser_decrescente():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")
    bidu = criar_animal("Bidu")

    registrar_atendimento(rex, "consulta_rotina")

    registrar_atendimento(mia, "consulta_rotina")
    registrar_atendimento(mia, "consulta_urgencia")

    registrar_atendimento(bidu, "consulta_urgencia")

    repositorio.adicionar(rex)
    repositorio.adicionar(mia)
    repositorio.adicionar(bidu)

    ranking = repositorio.ranking_por_total_gasto()

    totais = [animal.total_gasto() for animal in ranking]

    assert totais == [
        Decimal("280.00"),
        Decimal("180.00"),
        Decimal("100.00"),
    ]
    assert totais == sorted(totais, reverse=True)


def test_ranking_com_animais_sem_atendimentos():
    repositorio = AnimalRepositorio()
    sem_atendimento = criar_animal("Mia")
    com_atendimento = criar_animal("Rex")

    registrar_atendimento(com_atendimento, "consulta_rotina")

    repositorio.adicionar(sem_atendimento)
    repositorio.adicionar(com_atendimento)

    ranking = repositorio.ranking_por_total_gasto()

    assert ranking == [com_atendimento, sem_atendimento]
    assert sem_atendimento.total_gasto() == Decimal("0.00")


def test_ranking_lista_vazia():
    repositorio = AnimalRepositorio()

    assert repositorio.ranking_por_total_gasto() == []

def test_calcular_total_gasto_lista_animais():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")

    rex.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_rotina",
            valor=Decimal("100.00"),
        )
    )
    mia.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_urgencia",
            valor=Decimal("180.00"),
        )
    )

    repositorio.adicionar(rex)
    repositorio.adicionar(mia)

    total = repositorio.calcular_faturamento_total()

    assert total == Decimal("280.00")

def test_somar_faturamento_total_lista():
    repositorio = AnimalRepositorio()
    rex = criar_animal("Rex")
    mia = criar_animal("Mia")

    rex.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_rotina",
            valor=Decimal("100.00"),
        )
    )
    rex.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_urgencia",
            valor=Decimal("180.00"),
        )
    )
    mia.adicionar_atendimento(
        Atendimento(
            tipo_servico="consulta_emergencia",
            valor=Decimal("250.00"),
        )
    )

    repositorio.adicionar(rex)
    repositorio.adicionar(mia)

    faturamento = repositorio.calcular_faturamento_total()

    assert faturamento == Decimal("530.00")

def test_faturamento_lista_vazia_deve_ser_zero():
    repositorio = AnimalRepositorio()

    faturamento = repositorio.calcular_faturamento_total()

    assert faturamento == Decimal("0.00")
