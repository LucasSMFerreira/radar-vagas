import pytest
from sqlalchemy import text

from radar import banco
from radar.modelos import Vaga

pytestmark = pytest.mark.integracao


def vaga_teste(id_externo: str = "t1") -> Vaga:
    return Vaga(
        fonte="teste",
        id_externo=id_externo,
        titulo="Desenvolvedor Python Júnior",
        empresa="ACME",
        url="https://exemplo.com/vaga",
        descricao="FastAPI, SQL e Docker",
    )


@pytest.fixture(autouse=True)
def limpar():
    yield
    with banco.engine.begin() as conn:
        conn.execute(text("DELETE FROM vagas WHERE fonte = 'teste'"))


def test_vaga_repetida_nao_duplica():
    assert banco.salvar_vagas([vaga_teste()]) == 1
    assert banco.salvar_vagas([vaga_teste()]) == 0
    assert banco.salvar_vagas([vaga_teste("t2")]) == 1