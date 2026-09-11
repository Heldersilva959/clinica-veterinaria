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
) -> Atendimento:
    valor = calcular_valor_atendimento(
        tipo_servico,
        quantidade_atendimentos_anteriores=animal.quantidade_atendimentos(),
    )
    validar_valor_servico(valor)

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
    """Consulta de rotina do animal que da direito a retorno gratuito.

    A regra vale apenas para consulta de rotina e apenas para o historico
    do proprio animal. A data e sempre recebida de fora, nunca lida do
    relogio do sistema.
    """
    for atendimento in reversed(animal.atendimentos):
        if atendimento.tipo_servico != "consulta_rotina":
            continue

        if atendimento.data is None:
            continue

        if esta_dentro_do_periodo_de_retorno(atendimento.data, data_retorno):
            return atendimento

    return None


def registrar_retorno(animal: Animal, data_retorno: date) -> Atendimento:
    consulta = identificar_retorno(animal, data_retorno)

    if consulta is None:
        return registrar_atendimento(
            animal,
            "consulta_rotina",
            data=data_retorno,
        )

    valor = Decimal("0.00")
    validar_valor_final(valor)

    retorno = Atendimento(
        tipo_servico="retorno",
        valor=valor,
        data=data_retorno,
    )
    animal.adicionar_atendimento(retorno)

    return retorno
