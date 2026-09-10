from clinica.dominio.animal import Animal
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