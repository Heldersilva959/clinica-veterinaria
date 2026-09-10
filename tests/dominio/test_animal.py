from uuid import UUID

import pytest

from clinica.dominio.animal import Animal
from clinica.dominio.responsavel import Responsavel


def test_animal_deve_possuir_responsavel():
    with pytest.raises(
        ValueError,
        match="Animal deve possuir um responsável",
    ):
        Animal(nome="Rex", responsavel=None)


def test_animal_deve_iniciar_sem_atendimentos():
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Rex", responsavel=responsavel)

    assert animal.atendimentos == []


def test_nao_permitir_nome_animal_vazio():
    responsavel = Responsavel(nome="Maria")

    with pytest.raises(
        ValueError,
        match="Nome do animal não pode ser vazio",
    ):
        Animal(nome="", responsavel=responsavel)


def test_animal_deve_possuir_identificador():
    responsavel = Responsavel(nome="Maria")
    animal = Animal(
    nome="Rex",
    especie="cachorro",
    responsavel=responsavel,
)

    assert animal.id is not None
    assert isinstance(animal.id, UUID)