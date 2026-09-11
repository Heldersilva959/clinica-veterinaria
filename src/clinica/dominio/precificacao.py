from datetime import date
from decimal import ROUND_HALF_UP, Decimal

PERCENTUAL_DESCONTO_FIDELIDADE = Decimal("0.10")
ATENDIMENTOS_ANTERIORES_PARA_FIDELIDADE = 5
DIAS_PARA_RETORNO_GRATUITO = 15


def calcular_valor(tipo_servico: str) -> Decimal:
    if tipo_servico == "consulta_rotina":
        return Decimal("100.00")
    elif tipo_servico == "consulta_urgencia":
        return Decimal("180.00")
    elif tipo_servico == "consulta_emergencia":
        return Decimal("250.00")

    raise ValueError("Tipo de serviço inválido")


def validar_valor_servico(valor: Decimal) -> None:
    if valor <= Decimal("0.00"):
        raise ValueError("O valor do serviço deve ser maior que zero.")


def validar_valor_final(valor_final: Decimal) -> None:
    if valor_final < Decimal("0.00"):
        raise ValueError("O valor final não pode ser negativo.")


def validar_acrescimo(acrescimo: Decimal) -> None:
    if acrescimo < Decimal("0.00"):
        raise ValueError("O acréscimo não pode ser negativo.")


def validar_desconto(desconto: Decimal, valor: Decimal) -> None:
    if desconto < Decimal("0.00"):
        raise ValueError("O desconto não pode ser negativo.")

    if desconto > valor:
        raise ValueError(
            "O desconto não pode ser maior que o valor do atendimento."
        )


def arredondar(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def tem_desconto_fidelidade(quantidade_atendimentos_anteriores: int) -> bool:
    return (
        quantidade_atendimentos_anteriores
        >= ATENDIMENTOS_ANTERIORES_PARA_FIDELIDADE
    )


def aplicar_desconto_fidelidade(valor: Decimal) -> Decimal:
    desconto = valor * PERCENTUAL_DESCONTO_FIDELIDADE

    return arredondar(valor - desconto)


def somar_acrescimos(acrescimos: list[Decimal]) -> Decimal:
    return sum(acrescimos, Decimal("0.00"))


def calcular_valor_atendimento(
    tipo_servico: str,
    quantidade_atendimentos_anteriores: int = 0,
    acrescimo: Decimal = Decimal("0.00"),
) -> Decimal:
    validar_acrescimo(acrescimo)

    # O desconto de fidelidade incide sobre o total,
    # ou seja, sobre o valor base somado aos acrescimos.
    total = calcular_valor(tipo_servico) + acrescimo

    if tem_desconto_fidelidade(quantidade_atendimentos_anteriores):
        valor_final = aplicar_desconto_fidelidade(total)
    else:
        valor_final = arredondar(total)

    validar_valor_final(valor_final)

    return valor_final


def esta_dentro_do_periodo_de_retorno(
    data_consulta: date,
    data_retorno: date,
) -> bool:
    if data_retorno < data_consulta:
        return False

    return (data_retorno - data_consulta).days <= DIAS_PARA_RETORNO_GRATUITO
