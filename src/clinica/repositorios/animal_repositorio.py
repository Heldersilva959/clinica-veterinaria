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