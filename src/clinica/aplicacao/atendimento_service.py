from datetime import date
from decimal import Decimal
from uuid import UUID

from clinica.dominio.animal import Animal
from clinica.dominio.atendimento import Atendimento
from clinica.dominio.precificacao import calcular_valor_atendimento
from clinica.dominio.precificacao import esta_dentro_do_periodo_de_retorno
from clinica.dominio.precificacao import validar_valor_final
from clinica.dominio.precificacao import validar_valor_servico
from clinica.repositorios.animal_repositorio import AnimalRepositorio

def registrar_atendimento(
    animal: Animal,
    tipo_servico: str,
    data: date | None = None,
    acrescimo: Decimal = Decimal("0.00"),
) -> Atendimento:
    valor = calcular_valor_atendimento(
        tipo_servico,
        quantidade_atendimentos_anteriores=animal.quantidade_atendimentos(),
        acrescimo=acrescimo,
    )
    validar_valor_servico(valor)

    if data is not None and identificar_retorno(animal, data) is not None:
        return _registrar_atendimento_gratuito(animal, tipo_servico, data)

    atendimento = Atendimento(
        tipo_servico=tipo_servico,
        valor=valor,
        data=data,
    )
    animal.adicionar_atendimento(atendimento)

    return atendimento

def consultar_total_gasto(animal_id: UUID, repositorio: AnimalRepositorio) -> Decimal:
    animal = repositorio.buscar_por_id(animal_id)

    if animal is None:
        raise ValueError("Animal não encontrado")

    return animal.total_gasto()


def identificar_retorno(
    animal: Animal,
    data_retorno: date,
) -> Atendimento | None:
    """Atendimento que permite retorno no mesmo dia ou no seguinte.

    A regra considera somente o histórico do próprio animal. A data é sempre
    recebida de fora, nunca lida do relógio do sistema.
    """
    for atendimento in reversed(animal.atendimentos):
        if atendimento.data is None:
            continue

        if esta_dentro_do_periodo_de_retorno(atendimento.data, data_retorno):
            return atendimento

    return None


def _registrar_atendimento_gratuito(
    animal: Animal,
    tipo_servico: str,
    data_atendimento: date,
) -> Atendimento:
    valor = Decimal("0.00")
    validar_valor_final(valor)

    atendimento = Atendimento(
        tipo_servico=tipo_servico,
        valor=valor,
        data=data_atendimento,
    )
    animal.adicionar_atendimento(atendimento)

    return atendimento


def registrar_retorno(animal: Animal, data_retorno: date) -> Atendimento:
    consulta = identificar_retorno(animal, data_retorno)

    if consulta is None:
        return registrar_atendimento(
            animal,
            "consulta_rotina",
            data=data_retorno,
        )

    return _registrar_atendimento_gratuito(animal, "retorno", data_retorno)
