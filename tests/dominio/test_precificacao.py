from decimal import Decimal

import pytest

from clinica.dominio.precificacao import calcular_valor
from clinica.dominio.precificacao import validar_valor_servico


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