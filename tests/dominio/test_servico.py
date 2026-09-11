from decimal import Decimal

import pytest

from clinica.dominio.servico import Servico


def test_criar_servico_com_nome_e_valor():
    servico = Servico(
        nome="Vacinação",
        valor=Decimal("80.00"),
    )

    assert servico.nome == "Vacinação"
    assert servico.valor == Decimal("80.00")


def test_servico_nao_deve_possuir_nome_vazio():
    with pytest.raises(
        ValueError,
        match="Nome do serviço não pode ser vazio",
    ):
        Servico(
            nome="",
            valor=Decimal("80.00"),
        )


def test_servico_nao_deve_possuir_nome_apenas_com_espacos():
    with pytest.raises(
        ValueError,
        match="Nome do serviço não pode ser vazio",
    ):
        Servico(
            nome="   ",
            valor=Decimal("80.00"),
        )


def test_valor_servico_deve_ser_decimal():
    servico = Servico(
        nome="Vacinação",
        valor=Decimal("80.00"),
    )

    assert isinstance(servico.valor, Decimal)


def test_nao_permitir_valor_servico_zero():
    with pytest.raises(
        ValueError,
        match="Valor do serviço deve ser maior que zero",
    ):
        Servico(
            nome="Vacinação",
            valor=Decimal("0.00"),
        )


def test_nao_permitir_valor_servico_negativo():
    with pytest.raises(
        ValueError,
        match="Valor do serviço deve ser maior que zero",
    ):
        Servico(
            nome="Vacinação",
            valor=Decimal("-10.00"),
        )


def test_nao_permitir_valor_servico_com_float():
    with pytest.raises(
        TypeError,
        match="Valor do serviço deve ser Decimal",
    ):
        Servico(
            nome="Vacinação",
            valor=80.00,
        )
