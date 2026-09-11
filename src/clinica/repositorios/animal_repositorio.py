from decimal import Decimal
from uuid import UUID

from clinica.dominio.animal import Animal


class AnimalRepositorio:
    def __init__(self) -> None:
        self._animais: list[Animal] = []

    def listar(self) -> list[Animal]:
        return self._animais.copy()

    def adicionar(self, animal: Animal) -> None:
        animal_existente = self.buscar_por_id(animal.id)

        if animal_existente is not None:
            raise ValueError(
                "Animal com este identificador já cadastrado"
            )

        self._animais.append(animal)

    def buscar_por_nome(self, nome: str) -> Animal | None:
        for animal in self._animais:
            if animal.nome == nome:
                return animal

        return None

    def buscar_por_id(
        self,
        animal_id: UUID,
    ) -> Animal | None:
        for animal in self._animais:
            if animal.id == animal_id:
                return animal

        return None

    def remover(self, animal_id: UUID) -> None:
        animal = self.buscar_por_id(animal_id)

        if animal is not None:
            self._animais.remove(animal)

    def remover_animais_sem_atendimentos(self) -> None:
        self._animais = [
            animal
            for animal in self._animais
            if animal.quantidade_atendimentos() > 0
        ]

    def filtrar_por_especie(self, especie: str) -> list[Animal]:
        return [
            animal
            for animal in self._animais
            if animal.especie == especie
        ]

    def filtrar_por_gasto_acima_de(self, limite: Decimal) -> list[Animal]:
        return [
            animal
            for animal in self._animais
            if animal.total_gasto() > limite
        ]
    def ordenar_por_nome(self) -> None:
        self._animais.sort(
            key=lambda animal: animal.nome,
        )

    def ordenar_por_total_gasto(self) -> None:
        self._animais.sort(
            key=lambda animal: animal.total_gasto(),
        )

    def calcular_faturamento_total(self) -> Decimal:
        return sum(
            (animal.total_gasto() for animal in self._animais),
            Decimal("0.00"),
        )
