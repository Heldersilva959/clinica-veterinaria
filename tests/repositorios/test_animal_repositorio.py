from decimal import Decimal

from clinica.dominio.animal import Animal
from clinica.dominio.atendimento import Atendimento
from clinica.dominio.responsavel import Responsavel
from clinica.repositorios.animal_repositorio import AnimalRepositorio


def test_registrar_novo_animal_sem_atendimentos():
    repositorio = AnimalRepositorio()
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome="Rex", responsavel=responsavel)

    repositorio.adicionar(animal)

    animal_encontrado = repositorio.buscar_por_id(animal.id)

    assert animal_encontrado == animal
    assert animal_encontrado.atendimentos == []

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
