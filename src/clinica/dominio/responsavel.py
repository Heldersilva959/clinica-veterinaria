class Responsavel:
    def __init__(self, nome: str) -> None:
        if nome == "":
            raise ValueError("Nome do responsável não pode ser vazio")

        self.nome = nome
