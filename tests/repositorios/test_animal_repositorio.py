from uuid import uuid4
import pytest
from decimal import Decimal
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