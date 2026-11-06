from sqlalchemy import create_engine, text

from radar.config import DATABASE_URL
from radar.modelos import Vaga

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SQL_INSERIR = text("""
    INSERT INTO vagas (fonte, id_externo, titulo, empresa, local, url, descricao, publicada_em)
    VALUES (:fonte, :id_externo, :titulo, :empresa, :local, :url, :descricao, :publicada_em)
    ON CONFLICT (fonte, id_externo) DO NOTHING
    RETURNING id
""")


def salvar_vagas(vagas: list[Vaga]) -> int:
    """Grava as vagas e devolve quantas eram novas."""
    novas = 0
    with engine.begin() as conn:
        for vaga in vagas:
            if conn.execute(SQL_INSERIR, vaga.model_dump()).first() is not None:
                novas += 1
    return novas