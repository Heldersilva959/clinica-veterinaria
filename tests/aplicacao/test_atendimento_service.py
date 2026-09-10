from decimal import Decimal
from uuid import uuid4
import pytest

from clinica.aplicacao.atendimento_service import registrar_atendimento
from clinica.aplicacao.atendimento_service import consultar_total_gasto
from clinica.dominio.animal import Animal
from clinica.dominio.responsavel import Responsavel
from clinica.repositorios.animal_repositorio import AnimalRepositorio


def test_registrar_atendimento_para_animal():
    responsavel = Responsavel(nome="Maria")
    animal = Animal(
    nome="Rex",
    especie="cachorro",
    responsavel=responsavel,
)

    atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert atendimento.tipo_servico == "consulta_rotina"
    assert atendimento.valor == Decimal("100.00")
    assert atendimento in animal.atendimentos


def test_animal_deve_possuir_um_atendimento_apos_registro():

    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Mia", especie="gato", responsavel=responsavel)

    registrar_atendimento(animal, "consulta_urgencia")

    assert animal.quantidade_atendimentos() == 1
    assert animal.atendimentos[0].tipo_servico == "consulta_urgencia"


def test_registrar_multiplos_atendimentos_para_mesmo_animal():
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Mia", especie="gato", responsavel=responsavel)

    registrar_atendimento(animal, "consulta_rotina")
    registrar_atendimento(animal, "consulta_urgencia")
    registrar_atendimento(animal, "consulta_emergencia")

    assert animal.quantidade_atendimentos() == 3
    assert [atendimento.tipo_servico for atendimento in animal.atendimentos] == [
        "consulta_rotina",
        "consulta_urgencia",
        "consulta_emergencia",
    ]


def test_acumular_valores_varios_atendimentos():
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Mia", especie="gato", responsavel=responsavel)

    registrar_atendimento(animal, "consulta_rotina")
    registrar_atendimento(animal, "consulta_urgencia")
    registrar_atendimento(animal, "consulta_emergencia")

    assert animal.total_gasto() == Decimal("530.00")

def test_consultar_total_gasto_animal_existente():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(
        nome="Rex",
        especie="cachorro",
        responsavel=responsavel,
    )
    repositorio.adicionar(animal)
    registrar_atendimento(animal, "consulta_rotina")

    total = consultar_total_gasto(animal.id, repositorio)

    assert total == Decimal("100.00")


def test_animal_sem_atendimentos_deve_ter_total_zero():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(
        nome="Rex",
        especie="cachorro",
        responsavel=responsavel,
    )
    repositorio.adicionar(animal)

    total = consultar_total_gasto(animal.id, repositorio)

    assert total == Decimal("0.00")


def test_total_gasto_deve_considerar_todos_atendimentos():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(
        nome="Rex",
        especie="cachorro",
        responsavel=responsavel,
    )
    repositorio.adicionar(animal)

    registrar_atendimento(animal, "consulta_rotina")
    registrar_atendimento(animal, "consulta_urgencia")
    registrar_atendimento(animal, "consulta_emergencia")

    total = consultar_total_gasto(animal.id, repositorio)

    assert total == Decimal("530.00")


def test_animal_inexistente_lanca_excecao():
    repositorio = AnimalRepositorio()
    identificador_inexistente = uuid4()

    with pytest.raises(
        ValueError,
        match="Animal não encontrado",
    ):
        consultar_total_gasto(
            identificador_inexistente,
            repositorio,
        )