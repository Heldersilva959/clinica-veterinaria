import pytest

from clinica.dominio.responsavel import Responsavel


def test_nao_permitir_nome_responsavel_vazio():
    with pytest.raises(
        ValueError,
        match="Nome do responsável não pode ser vazio",
    ):
        Responsavel(nome="")