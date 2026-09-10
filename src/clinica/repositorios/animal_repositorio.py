from uuid import UUID

from clinica.dominio.animal import Animal


class AnimalRepositorio:
    def __init__(self) -> None:
        self._animais: list[Animal] = []

    def adicionar(self, animal: Animal) -> None:
        self._animais.append(animal)

    def buscar_por_id(self, animal_id: UUID) -> Animal | None:
        for animal in self._animais:
            if animal.id == animal_id:
                return animal

        return None

    def listar(self) -> list[Animal]:
        return list(self._animais)

    def remover_animais_sem_atendimentos(self) -> None:
        self._animais = [
            animal
            for animal in self._animais
            if animal.quantidade_atendimentos() > 0
        ]
