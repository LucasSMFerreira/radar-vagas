import json
from pathlib import Path

import httpx
import pytest
import respx

from radar.coletores import adzuna

FIXTURE = Path(__file__).parent / "fixtures" / "adzuna.json"


@pytest.fixture
def com_chave(monkeypatch):
    monkeypatch.setattr(adzuna, "ADZUNA_APP_ID", "id-falso")
    monkeypatch.setattr(adzuna, "ADZUNA_APP_KEY", "chave-falsa")


@respx.mock
def test_coletar_converte(com_chave):
    dados = json.loads(FIXTURE.read_text())
    respx.get(url__startswith=adzuna.URL).mock(
        return_value=httpx.Response(200, json=dados)
    )

    vagas = adzuna.coletar()

    assert len(vagas) == len(dados["results"])
    assert all(v.fonte == "adzuna" for v in vagas)


def test_sem_chave_falha_com_mensagem(monkeypatch):
    monkeypatch.setattr(adzuna, "ADZUNA_APP_ID", "")
    with pytest.raises(RuntimeError, match="ADZUNA"):
        adzuna.coletar()


def test_vaga_sem_empresa():
    item = {"id": 1, "title": "Dev <strong>Python</strong>", "redirect_url": "https://x"}
    vaga = adzuna.converter(item)
    assert vaga.empresa == "Não informada"
    assert vaga.titulo == "Dev Python"