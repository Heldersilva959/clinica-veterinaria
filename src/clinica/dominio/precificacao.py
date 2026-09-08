from decimal import Decimal


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