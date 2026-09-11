from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
import pytest

from clinica.aplicacao.atendimento_service import registrar_atendimento
from clinica.aplicacao.atendimento_service import consultar_total_gasto
from clinica.aplicacao.atendimento_service import identificar_retorno
from clinica.aplicacao.atendimento_service import registrar_retorno
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

def _criar_animal():
    responsavel = Responsavel(nome="Maria")

    return Animal(nome="Rex", especie="cachorro", responsavel=responsavel)


def test_primeiro_atendimento_nao_recebe_desconto():
    animal = _criar_animal()

    atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert atendimento.valor == Decimal("100.00")


def test_quarto_atendimento_nao_recebe_desconto():
    animal = _criar_animal()

    for _ in range(3):
        registrar_atendimento(animal, "consulta_rotina")

    quarto_atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert animal.quantidade_atendimentos() == 4
    assert quarto_atendimento.valor == Decimal("100.00")


def test_quinto_atendimento_nao_recebe_desconto():
    animal = _criar_animal()

    for _ in range(4):
        registrar_atendimento(animal, "consulta_rotina")

    quinto_atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert animal.quantidade_atendimentos() == 5
    assert quinto_atendimento.valor == Decimal("100.00")


def test_sexto_atendimento_recebe_desconto_fidelidade():
    animal = _criar_animal()

    for _ in range(5):
        registrar_atendimento(animal, "consulta_rotina")

    sexto_atendimento = registrar_atendimento(animal, "consulta_rotina")

    assert animal.quantidade_atendimentos() == 6
    assert sexto_atendimento.valor == Decimal("90.00")


# Regra de retorno (definida com o usuario):
# um retorno realizado ate 15 dias, inclusive, apos uma consulta de rotina
# do mesmo animal nao gera nova cobranca.

DATA_CONSULTA = date(2026, 3, 1)


def criar_animal_com_rotina(nome="Rex"):
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome=nome, especie="cachorro", responsavel=responsavel)

    registrar_atendimento(animal, "consulta_rotina", data=DATA_CONSULTA)

    return animal


def test_identificar_retorno_dentro_do_periodo():
    animal = criar_animal_com_rotina()

    consulta = identificar_retorno(animal, DATA_CONSULTA + timedelta(days=10))

    assert consulta is not None
    assert consulta is animal.atendimentos[0]
    assert consulta.tipo_servico == "consulta_rotina"

    assert identificar_retorno(animal, DATA_CONSULTA + timedelta(days=16)) is None

    animal_sem_rotina = Animal(
        nome="Mia",
        especie="gato",
        responsavel=Responsavel(nome="Maria"),
    )
    registrar_atendimento(
        animal_sem_rotina,
        "consulta_emergencia",
        data=DATA_CONSULTA,
    )

    assert identificar_retorno(animal_sem_rotina, DATA_CONSULTA) is None


def test_retorno_dentro_de_15_dias_nao_deve_ser_cobrado():
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=7))

    assert retorno.valor == Decimal("0.00")
    assert retorno in animal.atendimentos
    assert animal.total_gasto() == Decimal("100.00")


def test_retorno_com_exatos_15_dias_deve_ser_gratuito():
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=15))

    assert retorno.valor == Decimal("0.00")


def test_retorno_apos_15_dias_deve_ser_cobrado():
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=16))

    assert retorno.valor == Decimal("100.00")
    assert animal.total_gasto() == Decimal("200.00")


def test_retorno_deve_pertencer_ao_mesmo_animal():
    animal_atendido = criar_animal_com_rotina("Rex")
    outro_animal = Animal(
        nome="Mia",
        especie="gato",
        responsavel=Responsavel(nome="Maria"),
    )

    assert identificar_retorno(outro_animal, DATA_CONSULTA) is None

    retorno = registrar_retorno(outro_animal, DATA_CONSULTA + timedelta(days=5))

    assert retorno.valor == Decimal("100.00")
    assert len(animal_atendido.atendimentos) == 1
