from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Atendimento:
    tipo_servico: str
    valor: Decimal
    data: date | None = None
