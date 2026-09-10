from decimal import Decimal

import pytest

from clinica.dominio.precificacao import calcular_valor
from clinica.dominio.precificacao import validar_valor_servico
from clinica.dominio.precificacao import PERCENTUAL_DESCONTO_FIDELIDADE
from clinica.dominio.precificacao import aplicar_desconto_fidelidade
from clinica.dominio.precificacao import tem_desconto_fidelidade
from clinica.dominio.precificacao import calcular_valor_com_fidelidade

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

    valor = calcular_valor_com_fidelidade(
        "consulta_rotina",
        quantidade_atendimentos_anteriores=4,
    )

    assert valor == Decimal("100.00")


def test_calcular_atendimento_com_desconto():
    assert tem_desconto_fidelidade(5) is True

    valor = calcular_valor_com_fidelidade(
        "consulta_emergencia",
        quantidade_atendimentos_anteriores=5,
    )

    assert valor == Decimal("225.00")
    assert isinstance(valor, Decimal)
