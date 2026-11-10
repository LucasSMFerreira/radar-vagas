import httpx
from bs4 import BeautifulSoup

from radar.modelos import Vaga
from radar.texto import limpar_html


URL = "https://remotive.com/api/remote-jobs"
CABECALHOS = {"User-Agent": "radar-vagas (projeto de estudo)"}


def converter(item: dict) -> Vaga:
    return Vaga(
        fonte="remotive",
        id_externo=str(item["id"]),
        titulo=item["title"],
        empresa=item["company_name"],
        local=item.get("candidate_required_location") or None,
        url=item["url"],
        descricao=limpar_html(item.get("description", "")),
        publicada_em=item.get("publication_date"),
    )


def coletar() -> list[Vaga]:
    """Busca as vagas de desenvolvimento do Remotive (uma chamada só)."""
    resposta = httpx.get(
        URL, params={"category": "software-dev"}, headers=CABECALHOS, timeout=30
    )
    resposta.raise_for_status()
    return [converter(item) for item in resposta.json()["jobs"]]