from clinica.dominio.animal import Animal
from clinica.dominio.atendimento import Atendimento
from clinica.dominio.precificacao import calcular_valor
from clinica.dominio.precificacao import validar_valor_servico


def registrar_atendimento(animal: Animal, tipo_servico: str) -> Atendimento:
    valor = calcular_valor(tipo_servico)
    validar_valor_servico(valor)

    atendimento = Atendimento(tipo_servico=tipo_servico, valor=valor)
    animal.adicionar_atendimento(atendimento)

    return atendimento
