from decimal import Decimal
from uuid import UUID

from clinica.dominio.animal import Animal
from clinica.dominio.atendimento import Atendimento
from clinica.dominio.precificacao import calcular_valor
from clinica.dominio.precificacao import validar_valor_servico
from clinica.repositorios.animal_repositorio import AnimalRepositorio

def registrar_atendimento(animal: Animal, tipo_servico: str) -> Atendimento:
    valor = calcular_valor(tipo_servico)
    validar_valor_servico(valor)

    atendimento = Atendimento(tipo_servico=tipo_servico, valor=valor)
    animal.adicionar_atendimento(atendimento)

    return atendimento

def consultar_total_gasto(animal_id: UUID, repositorio: AnimalRepositorio) -> Decimal:
    animal = repositorio.buscar_por_id(animal_id)

    if animal is None:
        raise ValueError("Animal não encontrado")

    return animal.total_gasto()