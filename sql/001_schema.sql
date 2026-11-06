CREATE TABLE IF NOT EXISTS vagas (
    id           BIGSERIAL PRIMARY KEY,
    fonte        TEXT NOT NULL,
    id_externo   TEXT NOT NULL,
    titulo       TEXT NOT NULL,
    empresa      TEXT NOT NULL,
    local        TEXT,
    url          TEXT NOT NULL,
    descricao    TEXT NOT NULL,
    publicada_em TIMESTAMPTZ,
    coletada_em  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (fonte, id_externo)
);

CREATE INDEX IF NOT EXISTS idx_vagas_coletada_em ON vagas (coletada_em);