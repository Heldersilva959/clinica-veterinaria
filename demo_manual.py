"""Demonstração manual do sistema da clínica veterinária no terminal."""

from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
import sys


# Permite executar o arquivo diretamente da raiz sem instalar o pacote.
RAIZ_PROJETO = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ_PROJETO / "src"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from clinica.aplicacao.atendimento_service import (  # noqa: E402
    consultar_total_gasto,
    registrar_atendimento,
)
from clinica.dominio.animal import Animal  # noqa: E402
from clinica.dominio.responsavel import Responsavel  # noqa: E402
from clinica.dominio.servico import Servico, obter_servico  # noqa: E402
from clinica.repositorios.animal_repositorio import (  # noqa: E402
    AnimalRepositorio,
)


LARGURA = 96


def moeda(valor: Decimal) -> str:
    numero = f"{valor.quantize(Decimal('0.01')):.2f}".replace(".", ",")
    return f"R$ {numero}"


def data_formatada(valor: date | None) -> str:
    return valor.strftime("%d/%m/%Y") if valor is not None else "-"


def cabecalho(titulo: str, subtitulo: str = "") -> None:
    print("\n" + "╔" + "═" * (LARGURA - 2) + "╗")
    print("║" + titulo.center(LARGURA - 2) + "║")
    if subtitulo:
        print("║" + subtitulo.center(LARGURA - 2) + "║")
    print("╚" + "═" * (LARGURA - 2) + "╝")


def secao(titulo: str) -> None:
    print("\n" + "┌" + "─" * (LARGURA - 2) + "┐")
    print("│ " + titulo.ljust(LARGURA - 4) + " │")
    print("└" + "─" * (LARGURA - 2) + "┘")


def tabela(cabecalhos: list[str], linhas: list[list[object]]) -> None:
    textos = [[str(valor) for valor in linha] for linha in linhas]
    larguras = [
        max(
            len(cabecalho),
            *(len(linha[indice]) for linha in textos),
        )
        for indice, cabecalho in enumerate(cabecalhos)
    ]

    separador = "+-" + "-+-".join("-" * largura for largura in larguras) + "-+"

    def exibir_linha(valores: list[str]) -> None:
        celulas = [
            valor.ljust(larguras[indice])
            for indice, valor in enumerate(valores)
        ]
        print("| " + " | ".join(celulas) + " |")

    print(separador)
    exibir_linha(cabecalhos)
    print(separador)
    for linha in textos:
        exibir_linha(linha)
    print(separador)


def nomes(animais: list[Animal]) -> str:
    return ", ".join(animal.nome for animal in animais) or "Nenhum"


def criar_animal_para_retorno(
    nome: str,
    data_consulta: date,
    quantidade_atendimentos_anteriores: int = 1,
) -> Animal:
    animal = Animal(
        nome=nome,
        especie="cachorro",
        responsavel=Responsavel(nome="Responsável do teste"),
    )
    registrar_atendimento(
        animal,
        "consulta_rotina",
        data=data_consulta,
    )

    for _ in range(quantidade_atendimentos_anteriores - 1):
        registrar_atendimento(animal, "consulta_rotina")

    return animal


def main() -> None:
    cabecalho(
        "CLÍNICA VETERINÁRIA - DEMONSTRAÇÃO MANUAL",
        "Sistema em memória | Python + TDD + Pytest",
    )

    secao("1. Catálogo de serviços")
    tipos = [
        "consulta_rotina",
        "consulta_urgencia",
        "consulta_emergencia",
    ]
    tabela(
        ["Código", "Valor"],
        [
            [tipo, moeda(obter_servico(tipo).valor)]
            for tipo in tipos
        ],
    )

    servico_personalizado = Servico(
        nome="vacina_v10",
        valor=Decimal("85.00"),
    )
    print(
        "[OK] Serviço personalizado validado pelo domínio: "
        f"{servico_personalizado.nome} - {moeda(servico_personalizado.valor)}"
    )

    secao("2. Cadastro de responsáveis e animais")
    maria = Responsavel(nome="Maria")
    joao = Responsavel(nome="João")

    rex = Animal(nome="Rex", especie="cachorro", responsavel=maria)
    mia = Animal(nome="Mia", especie="gato", responsavel=joao)
    luna = Animal(nome="Luna", especie="gato", responsavel=maria)
    nina = Animal(nome="Nina", especie="coelho", responsavel=joao)

    repositorio = AnimalRepositorio()
    for animal in (rex, mia, luna, nina):
        repositorio.adicionar(animal)

    tabela(
        ["Animal", "Espécie", "Responsável", "Identificador"],
        [
            [
                animal.nome,
                animal.especie,
                animal.responsavel.nome,
                animal.id,
            ]
            for animal in repositorio.listar()
        ],
    )

    secao("3. Registro, retorno automático, fidelidade e acréscimo")
    data_inicial = date(2026, 9, 1)

    datas_rex = [
        data_inicial,
        data_inicial,
        data_inicial + timedelta(days=1),
        data_inicial + timedelta(days=3),
        data_inicial + timedelta(days=5),
        data_inicial + timedelta(days=7),
    ]
    valores_rex: list[Decimal] = []
    for data_atendimento in datas_rex:
        atendimento = registrar_atendimento(
            rex,
            "consulta_rotina",
            data=data_atendimento,
        )
        valores_rex.append(atendimento.valor)

    registrar_atendimento(
        mia,
        "consulta_urgencia",
        data=date(2026, 9, 3),
    )
    registrar_atendimento(
        mia,
        "consulta_emergencia",
        data=date(2026, 9, 4),
    )
    atendimento_com_acrescimo = registrar_atendimento(
        luna,
        "consulta_rotina",
        data=date(2026, 9, 5),
        acrescimo=Decimal("35.50"),
    )
    linhas_atendimentos: list[list[object]] = []
    for animal in repositorio.listar():
        for numero, atendimento in enumerate(animal.atendimentos, start=1):
            linhas_atendimentos.append(
                [
                    animal.nome,
                    numero,
                    atendimento.tipo_servico,
                    data_formatada(atendimento.data),
                    moeda(atendimento.valor),
                ]
            )

    tabela(
        ["Animal", "Nº", "Serviço", "Data", "Valor cobrado"],
        linhas_atendimentos,
    )
    print("[OK] Mesmo dia e dia seguinte registrados automaticamente como retorno")
    print(f"[OK] Sexto atendimento de Rex com fidelidade: {moeda(valores_rex[-1])}")
    print("[OK] Emergência de Mia no dia seguinte registrada como retorno gratuito")
    print(f"[OK] Consulta de Luna com acréscimo: {moeda(atendimento_com_acrescimo.valor)}")

    secao("4. Retorno: gratuito no mesmo dia ou no dia seguinte")
    data_consulta_retorno = date(2026, 10, 1)
    configuracoes_retorno = [
        ("Data anterior", -1, Decimal("100.00")),
        ("Mesmo dia", 0, Decimal("0.00")),
        ("Dia seguinte", 1, Decimal("0.00")),
        ("Dois dias depois", 2, Decimal("100.00")),
        ("Sete dias depois", 7, Decimal("100.00")),
        ("Trinta dias depois", 30, Decimal("100.00")),
    ]
    linhas_retorno: list[list[object]] = []
    resultados_retorno: list[tuple[Decimal, Decimal]] = []

    for indice, (cenario, dias, esperado) in enumerate(
        configuracoes_retorno,
        start=1,
    ):
        animal_retorno = criar_animal_para_retorno(
            nome=f"Retorno {indice}",
            data_consulta=data_consulta_retorno,
        )
        data_retorno = data_consulta_retorno + timedelta(days=dias)
        retorno = registrar_atendimento(
            animal_retorno,
            "consulta_rotina",
            data=data_retorno,
        )
        resultados_retorno.append((retorno.valor, esperado))
        linhas_retorno.append(
            [
                cenario,
                data_formatada(data_consulta_retorno),
                data_formatada(data_retorno),
                1,
                moeda(esperado),
                moeda(retorno.valor),
                "OK" if retorno.valor == esperado else "FALHOU",
            ]
        )

    animal_fiel_gratis = criar_animal_para_retorno(
        nome="Fiel grátis",
        data_consulta=data_consulta_retorno,
        quantidade_atendimentos_anteriores=5,
    )
    retorno_fiel_gratis = registrar_atendimento(
        animal_fiel_gratis,
        "consulta_emergencia",
        data=data_consulta_retorno + timedelta(days=1),
    )
    linhas_retorno.append(
        [
            "Dia seguinte + fidelidade",
            data_formatada(data_consulta_retorno),
            data_formatada(data_consulta_retorno + timedelta(days=1)),
            5,
            moeda(Decimal("0.00")),
            moeda(retorno_fiel_gratis.valor),
            "OK" if retorno_fiel_gratis.valor == Decimal("0.00") else "FALHOU",
        ]
    )

    animal_fiel_cobrado = criar_animal_para_retorno(
        nome="Fiel cobrado",
        data_consulta=data_consulta_retorno,
        quantidade_atendimentos_anteriores=5,
    )
    retorno_fiel_cobrado = registrar_atendimento(
        animal_fiel_cobrado,
        "consulta_rotina",
        data=data_consulta_retorno + timedelta(days=2),
    )
    linhas_retorno.append(
        [
            "Dois dias + fidelidade",
            data_formatada(data_consulta_retorno),
            data_formatada(data_consulta_retorno + timedelta(days=2)),
            5,
            moeda(Decimal("90.00")),
            moeda(retorno_fiel_cobrado.valor),
            "OK" if retorno_fiel_cobrado.valor == Decimal("90.00") else "FALHOU",
        ]
    )

    tabela(
        [
            "Cenário",
            "Consulta",
            "Retorno",
            "Anteriores",
            "Esperado",
            "Cobrado",
            "Status",
        ],
        linhas_retorno,
    )

    secao("5. Totais por animal")
    tabela(
        ["Animal", "Atendimentos", "Total gasto"],
        [
            [
                animal.nome,
                animal.quantidade_atendimentos(),
                moeda(consultar_total_gasto(animal.id, repositorio)),
            ]
            for animal in repositorio.listar()
        ],
    )

    secao("6. Consultas, filtros e ranking")
    encontrado_nome = repositorio.buscar_por_nome("Rex")
    encontrado_id = repositorio.buscar_por_id(mia.id)
    gatos = repositorio.filtrar_por_especie("gato")
    acima_de_200 = repositorio.filtrar_por_gasto_acima_de(Decimal("200.00"))
    ranking = repositorio.ranking_por_total_gasto()
    faturamento = repositorio.calcular_faturamento_total()

    print(f"Busca por nome 'Rex': {encontrado_nome.nome if encontrado_nome else 'Não encontrado'}")
    print(f"Busca pelo ID de Mia: {encontrado_id.nome if encontrado_id else 'Não encontrado'}")
    print(f"Filtro por espécie 'gato': {nomes(gatos)}")
    print(f"Gasto acima de R$ 200,00: {nomes(acima_de_200)}")
    print(f"Ranking decrescente: {nomes(ranking)}")
    print(f"Faturamento total: {moeda(faturamento)}")

    secao("7. Remoção e ordenações")
    print(f"Antes de remover animais sem atendimento: {nomes(repositorio.listar())}")
    repositorio.remover_animais_sem_atendimentos()
    print(f"Depois da remoção: {nomes(repositorio.listar())}")

    repositorio.ordenar_por_nome()
    print(f"Ordenação por nome: {nomes(repositorio.listar())}")

    repositorio.ordenar_por_total_gasto()
    print(f"Ordenação por total crescente: {nomes(repositorio.listar())}")

    assert valores_rex == [
        Decimal("100.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("100.00"),
        Decimal("100.00"),
        Decimal("90.00"),
    ]
    assert all(real == esperado for real, esperado in resultados_retorno)
    assert retorno_fiel_gratis.valor == Decimal("0.00")
    assert retorno_fiel_cobrado.valor == Decimal("90.00")
    assert atendimento_com_acrescimo.valor == Decimal("135.50")
    assert faturamento == Decimal("705.50")
    assert ranking == [rex, mia, luna, nina]
    assert repositorio.buscar_por_id(nina.id) is None

    cabecalho(
        "DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO",
        "Todos os resultados internos foram verificados.",
    )


if __name__ == "__main__":
    main()
