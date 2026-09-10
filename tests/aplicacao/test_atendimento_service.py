from decimal import Decimal

from clinica.aplicacao.atendimento_service import registrar_atendimento
from clinica.dominio.animal import Animal


def test_registrar_atendimento_para_animal():
    animal = Animal(nome="Rex", especie="cachorro")

    atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert atendimento.tipo_servico == "consulta_rotina"
    assert atendimento.valor == Decimal("100.00")
    assert atendimento in animal.atendimentos


def test_animal_deve_possuir_um_atendimento_apos_registro():
    animal = Animal(nome="Mia", especie="gato")

    registrar_atendimento(animal, "consulta_urgencia")

    assert animal.quantidade_atendimentos() == 1
    assert animal.atendimentos[0].tipo_servico == "consulta_urgencia"


def test_registrar_multiplos_atendimentos_para_mesmo_animal():
    animal = Animal(nome="Bidu", especie="cachorro")

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
    animal = Animal(nome="Luna", especie="gato")

    registrar_atendimento(animal, "consulta_rotina")
    registrar_atendimento(animal, "consulta_urgencia")
    registrar_atendimento(animal, "consulta_emergencia")

    assert animal.total_gasto() == Decimal("530.00")
