from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Servico:
    nome: str
    valor: Decimal

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise ValueError("Nome do serviço não pode ser vazio")

        if not isinstance(self.valor, Decimal):
            raise TypeError("Valor do serviço deve ser Decimal")

        if self.valor <= Decimal("0.00"):
            raise ValueError("Valor do serviço deve ser maior que zero")


_SERVICOS: dict[str, Servico] = {
    "consulta_rotina": Servico(
        nome="consulta_rotina",
        valor=Decimal("100.00"),
    ),
    "consulta_urgencia": Servico(
        nome="consulta_urgencia",
        valor=Decimal("180.00"),
    ),
    "consulta_emergencia": Servico(
        nome="consulta_emergencia",
        valor=Decimal("250.00"),
    ),
}


def obter_servico(tipo_servico: str) -> Servico:
    try:
        return _SERVICOS[tipo_servico]
    except KeyError as erro:
        raise ValueError("Tipo de serviço inválido") from erro
