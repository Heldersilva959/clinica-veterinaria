from decimal import Decimal

import pytest

from clinica.dominio.precificacao import calcular_valor
from clinica.dominio.precificacao import validar_valor_servico
from clinica.dominio.precificacao import PERCENTUAL_DESCONTO_FIDELIDADE
from clinica.dominio.precificacao import aplicar_desconto_fidelidade
from clinica.dominio.precificacao import tem_desconto_fidelidade
from clinica.dominio.precificacao import calcular_valor_atendimento
from clinica.dominio.precificacao import validar_valor_final
from clinica.dominio.precificacao import validar_acrescimo
from clinica.dominio.precificacao import validar_desconto


def test_calcular_valor_consulta_rotina():
    valor = calcular_valor("consulta_rotina")

    assert valor == Decimal('100.00')

def test_calcular_valor_consulta_urgencia():
    valor = calcular_valor("consulta_urgencia")

    assert valor == Decimal('180.00')

def test_calcular_valor_atendimento_emergencia():
    valor = calcular_valor("consulta_emergencia")

    assert valor == Decimal('250.00')


def test_nao_permitir_valor_servico_zero():
    with pytest.raises(ValueError):
        validar_valor_servico(Decimal("0.00"))

def test_nao_permitir_valor_servico_negativo():
    with pytest.raises(ValueError):
        validar_valor_servico(Decimal("-10.00"))

def test_calcular_valores_decimais():
    valor = calcular_valor("consulta_urgencia")

    assert isinstance(valor, Decimal)
    assert valor == Decimal("180.00")

def test_tipo_servico_invalido_lanca_excecao():
    with pytest.raises(
        ValueError,
        match="Tipo de serviço inválido",
    ):
        calcular_valor("servico_inexistente")

def test_desconto_fidelidade_deve_ser_de_dez_porcento():
    assert PERCENTUAL_DESCONTO_FIDELIDADE == Decimal("0.10")


def test_aplicar_desconto_fidelidade():
    assert aplicar_desconto_fidelidade(Decimal("100.00")) == Decimal("90.00")
    assert aplicar_desconto_fidelidade(Decimal("180.00")) == Decimal("162.00")
    assert aplicar_desconto_fidelidade(Decimal("250.00")) == Decimal("225.00")


def test_nao_aplicar_desconto_sem_fidelidade():
    assert tem_desconto_fidelidade(0) is False
    assert tem_desconto_fidelidade(4) is False

    valor = calcular_valor_atendimento(
        "consulta_rotina",
        quantidade_atendimentos_anteriores=4,
    )

    assert valor == Decimal("100.00")


def test_calcular_atendimento_com_desconto():
    assert tem_desconto_fidelidade(5) is True

    valor = calcular_valor_atendimento(
        "consulta_emergencia",
        quantidade_atendimentos_anteriores=5,
    )

    assert valor == Decimal("225.00")
    assert isinstance(valor, Decimal)


def test_atendimento_sem_adicional_nao_deve_ter_acrescimo():
    valor = calcular_valor_atendimento("consulta_rotina")

    assert valor == Decimal("100.00")

    valor_com_acrescimo_zero = calcular_valor_atendimento(
        "consulta_rotina",
        acrescimo=Decimal("0.00"),
    )

    assert valor_com_acrescimo_zero == Decimal("100.00")


def test_aplicar_acrescimo_procedimento_adicional():
    valor = calcular_valor_atendimento(
        "consulta_rotina",
        acrescimo=Decimal("50.00"),
    )

    assert valor == Decimal("150.00")
    assert isinstance(valor, Decimal)


def test_calcular_atendimento_com_desconto_e_acrescimo():
    # Regra definida: o desconto de fidelidade incide sobre o total,
    # ou seja, sobre o valor base somado aos acrescimos.
    valor = calcular_valor_atendimento(
        "consulta_rotina",
        quantidade_atendimentos_anteriores=5,
        acrescimo=Decimal("50.00"),
    )

    assert valor == Decimal("135.00")

    valor_sem_fidelidade = calcular_valor_atendimento(
        "consulta_rotina",
        quantidade_atendimentos_anteriores=4,
        acrescimo=Decimal("50.00"),
    )

    assert valor_sem_fidelidade == Decimal("150.00")


def test_nao_permitir_valor_negativo():
    with pytest.raises(
        ValueError,
        match="O valor final não pode ser negativo.",
    ):
        validar_valor_final(Decimal("-0.01"))

    validar_valor_final(Decimal("0.00"))


def test_acrescimo_negativo_deve_ser_rejeitado():
    with pytest.raises(
        ValueError,
        match="O acréscimo não pode ser negativo.",
    ):
        validar_acrescimo(Decimal("-10.00"))

    with pytest.raises(
        ValueError,
        match="O acréscimo não pode ser negativo.",
    ):
        calcular_valor_atendimento(
            "consulta_rotina",
            acrescimo=Decimal("-10.00"),
        )


def test_desconto_negativo_deve_ser_rejeitado():
    with pytest.raises(
        ValueError,
        match="O desconto não pode ser negativo.",
    ):
        validar_desconto(Decimal("-1.00"), Decimal("100.00"))


def test_desconto_nao_pode_superar_valor_atendimento():
    with pytest.raises(
        ValueError,
        match="O desconto não pode ser maior que o valor do atendimento.",
    ):
        validar_desconto(Decimal("150.00"), Decimal("100.00"))

    validar_desconto(Decimal("100.00"), Decimal("100.00"))


def test_valor_final_deve_possuir_duas_casas_decimais():
    valores = [
        calcular_valor_atendimento("consulta_rotina"),
        calcular_valor_atendimento(
            "consulta_urgencia",
            quantidade_atendimentos_anteriores=5,
        ),
        calcular_valor_atendimento(
            "consulta_emergencia",
            quantidade_atendimentos_anteriores=5,
            acrescimo=Decimal("33.33"),
        ),
        aplicar_desconto_fidelidade(Decimal("99.99")),
    ]

    for valor in valores:
        assert isinstance(valor, Decimal)
        assert valor.as_tuple().exponent == -2
