import httpx

from radar.config import ADZUNA_APP_ID, ADZUNA_APP_KEY, PALAVRAS_CHAVE
from radar.modelos import Vaga
from radar.texto import limpar_html

URL = "https://api.adzuna.com/v1/api/jobs/br/search/1"


def converter(item: dict) -> Vaga:
    return Vaga(
        fonte="adzuna",
        id_externo=str(item["id"]),
        titulo=limpar_html(item["title"]),
        empresa=item.get("company", {}).get("display_name") or "Não informada",
        local=item.get("location", {}).get("display_name"),
        url=item["redirect_url"],
        descricao=limpar_html(item.get("description", "")),
        publicada_em=item.get("created"),
    )


def coletar() -> list[Vaga]:
    """Busca vagas recentes no Brasil com qualquer uma das palavras-chave."""
    if not (ADZUNA_APP_ID and ADZUNA_APP_KEY):
        raise RuntimeError("Defina ADZUNA_APP_ID e ADZUNA_APP_KEY no .env")
    resposta = httpx.get(
        URL,
        params={
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what_or": PALAVRAS_CHAVE,
            "max_days_old": 7,
            "sort_by": "date",
            "results_per_page": 50,
            "content-type": "application/json",
        },
        timeout=30,
    )
    resposta.raise_for_status()
    return [converter(item) for item in resposta.json()["results"]]