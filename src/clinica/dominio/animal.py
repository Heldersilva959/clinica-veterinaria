from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from clinica.dominio.atendimento import Atendimento
from clinica.dominio.responsavel import Responsavel


@dataclass
class Animal:
    nome: str
    responsavel: Responsavel
    especie: str = ""
    id: UUID = field(default_factory=uuid4, init=False)
    atendimentos: list[Atendimento] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.responsavel is None:
            raise ValueError("Animal deve possuir um responsável")

        if self.nome == "":
            raise ValueError("Nome do animal não pode ser vazio")

    def adicionar_atendimento(self, atendimento: Atendimento) -> None:
        self.atendimentos.append(atendimento)

    def quantidade_atendimentos(self) -> int:
        return len(self.atendimentos)

    def total_gasto(self) -> Decimal:
        return sum(
            (atendimento.valor for atendimento in self.atendimentos),
            Decimal("0.00"),
        )
