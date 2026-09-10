from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal

from clinica.dominio.atendimento import Atendimento


@dataclass
class Animal:
    nome: str
    especie: str = ""
    atendimentos: list[Atendimento] = field(default_factory=list)

    def adicionar_atendimento(self, atendimento: Atendimento) -> None:
        self.atendimentos.append(atendimento)

    def quantidade_atendimentos(self) -> int:
        return len(self.atendimentos)

    def total_gasto(self) -> Decimal:
        return sum(
            (atendimento.valor for atendimento in self.atendimentos),
            Decimal("0.00"),
        )
