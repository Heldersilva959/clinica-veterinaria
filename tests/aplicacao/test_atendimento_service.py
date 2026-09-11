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


def test_registrar_atendimento_com_acrescimo():
    animal = Animal(
        nome="Rex",
        especie="cachorro",
        responsavel=Responsavel(nome="Maria"),
    )

    atendimento = registrar_atendimento(
        animal,
        "consulta_rotina",
        acrescimo=Decimal("35.50"),
    )

    assert atendimento.valor == Decimal("135.50")
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


# Regra de retorno (definida com o usuário):
# um novo atendimento no mesmo dia ou no dia seguinte a qualquer atendimento
# do mesmo animal é registrado como retorno e não gera nova cobrança.

DATA_CONSULTA = date(2026, 3, 1)


def criar_animal_com_rotina(nome="Rex"):
    responsavel = Responsavel(nome="Maria")
    animal = Animal(nome=nome, especie="cachorro", responsavel=responsavel)

    registrar_atendimento(animal, "consulta_rotina", data=DATA_CONSULTA)

    return animal


def test_identificar_retorno_dentro_do_periodo():
    animal = criar_animal_com_rotina()

    consulta_mesmo_dia = identificar_retorno(animal, DATA_CONSULTA)
    consulta_dia_seguinte = identificar_retorno(
        animal,
        DATA_CONSULTA + timedelta(days=1),
    )

    assert consulta_mesmo_dia is animal.atendimentos[0]
    assert consulta_dia_seguinte is animal.atendimentos[0]
    assert consulta_mesmo_dia.tipo_servico == "consulta_rotina"

    assert identificar_retorno(animal, DATA_CONSULTA + timedelta(days=2)) is None
    assert identificar_retorno(animal, DATA_CONSULTA - timedelta(days=1)) is None

    animal_com_emergencia = Animal(
        nome="Mia",
        especie="gato",
        responsavel=Responsavel(nome="Maria"),
    )
    registrar_atendimento(
        animal_com_emergencia,
        "consulta_emergencia",
        data=DATA_CONSULTA,
    )

    atendimento_anterior = identificar_retorno(
        animal_com_emergencia,
        DATA_CONSULTA + timedelta(days=1),
    )

    assert atendimento_anterior is animal_com_emergencia.atendimentos[0]


def test_servico_diferente_no_dia_seguinte_deve_ser_retorno_gratuito():
    animal = _criar_animal()
    registrar_atendimento(
        animal,
        "consulta_urgencia",
        data=DATA_CONSULTA,
    )

    retorno = registrar_atendimento(
        animal,
        "consulta_emergencia",
        data=DATA_CONSULTA + timedelta(days=1),
    )

    assert retorno.tipo_servico == "consulta_emergencia"
    assert retorno.valor == Decimal("0.00")
    assert animal.total_gasto() == Decimal("180.00")


def test_retorno_deve_permitir_novo_retorno_no_dia_seguinte():
    animal = criar_animal_com_rotina()
    primeiro_retorno = registrar_atendimento(
        animal,
        "consulta_rotina",
        data=DATA_CONSULTA,
    )

    segundo_retorno = registrar_atendimento(
        animal,
        "consulta_emergencia",
        data=DATA_CONSULTA + timedelta(days=1),
    )

    assert primeiro_retorno.valor == Decimal("0.00")
    assert segundo_retorno.tipo_servico == "consulta_emergencia"
    assert segundo_retorno.valor == Decimal("0.00")
    assert animal.total_gasto() == Decimal("100.00")


@pytest.mark.parametrize("dias_apos_consulta", [0, 1])
def test_registrar_novo_atendimento_de_rotina_identifica_retorno_gratuito(
    dias_apos_consulta,
):
    animal = criar_animal_com_rotina()

    retorno = registrar_atendimento(
        animal,
        "consulta_rotina",
        data=DATA_CONSULTA + timedelta(days=dias_apos_consulta),
    )

    assert retorno.tipo_servico == "consulta_rotina"
    assert retorno.valor == Decimal("0.00")
    assert animal.total_gasto() == Decimal("100.00")


def test_registrar_novo_atendimento_de_rotina_apos_dois_dias_deve_ser_cobrado():
    animal = criar_animal_com_rotina()

    atendimento = registrar_atendimento(
        animal,
        "consulta_rotina",
        data=DATA_CONSULTA + timedelta(days=2),
    )

    assert atendimento.tipo_servico == "consulta_rotina"
    assert atendimento.valor == Decimal("100.00")
    assert animal.total_gasto() == Decimal("200.00")


def test_retorno_no_mesmo_dia_nao_deve_ser_cobrado():
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, DATA_CONSULTA)

    assert retorno.valor == Decimal("0.00")
    assert retorno in animal.atendimentos
    assert animal.total_gasto() == Decimal("100.00")


def test_retorno_no_dia_seguinte_nao_deve_ser_cobrado():
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=1))

    assert retorno.valor == Decimal("0.00")
    assert retorno in animal.atendimentos
    assert animal.total_gasto() == Decimal("100.00")


@pytest.mark.parametrize(
    "data_retorno",
    [
        DATA_CONSULTA - timedelta(days=1),
        DATA_CONSULTA + timedelta(days=2),
        DATA_CONSULTA + timedelta(days=7),
        DATA_CONSULTA + timedelta(days=30),
    ],
)
def test_retorno_fora_do_periodo_gratuito_deve_ser_cobrado(data_retorno):
    animal = criar_animal_com_rotina()

    retorno = registrar_retorno(animal, data_retorno)

    assert retorno.valor == Decimal("100.00")
    assert animal.total_gasto() == Decimal("200.00")


def test_retorno_no_dia_seguinte_continua_gratuito_com_fidelidade():
    animal = criar_animal_com_rotina()

    for _ in range(4):
        registrar_atendimento(animal, "consulta_rotina")

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=1))

    assert animal.quantidade_atendimentos() == 6
    assert retorno.valor == Decimal("0.00")
    assert animal.total_gasto() == Decimal("500.00")


def test_retorno_fora_do_prazo_com_fidelidade_recebe_desconto():
    animal = criar_animal_com_rotina()

    for _ in range(4):
        registrar_atendimento(animal, "consulta_rotina")

    retorno = registrar_retorno(animal, DATA_CONSULTA + timedelta(days=2))

    assert animal.quantidade_atendimentos() == 6
    assert retorno.valor == Decimal("90.00")
    assert animal.total_gasto() == Decimal("590.00")


def test_retorno_deve_pertencer_ao_mesmo_animal():
    animal_atendido = criar_animal_com_rotina("Rex")
    outro_animal = Animal(
        nome="Mia",
        especie="gato",
        responsavel=Responsavel(nome="Maria"),
    )

    assert identificar_retorno(outro_animal, DATA_CONSULTA) is None

    retorno = registrar_retorno(outro_animal, DATA_CONSULTA + timedelta(days=1))

    assert retorno.valor == Decimal("100.00")
    assert len(animal_atendido.atendimentos) == 1
