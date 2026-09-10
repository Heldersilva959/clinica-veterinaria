from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Atendimento:
    tipo_servico: str
    valor: Decimal
