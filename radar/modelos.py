from datetime import datetime

from pydantic import BaseModel


class Vaga(BaseModel):
    """Uma vaga já normalizada, igual para todas as fontes."""

    fonte: str
    id_externo: str
    titulo: str
    empresa: str
    local: str | None = None
    url: str
    descricao: str
    publicada_em: datetime | None = None