import json
from pathlib import Path

import httpx
import pytest
import respx

from radar.coletores import remotive

FIXTURE = Path(__file__).parent / "fixtures" / "remotive.json"



@respx.mock
def test_coletar_erro_do_servidor():
    """Erro da API aparece, em vez de virar lista vazia."""
    respx.get(url__startswith=remotive.URL).mock(return_value=httpx.Response(500))

    vagas = remotive.coletar()

    assert len(vagas) == len(dados["jobs"])
    assert vagas[0].fonte == "remotive"
    assert vagas[0].id_externo == str(dados["jobs"][0]["id"])
    assert "<" not in vagas[0].descricao


@respx.mock
def test_coletar_erro_do_servidor():
    respx.get(url__startswith=remotive.URL).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPStatusError):
        remotive.coletar()