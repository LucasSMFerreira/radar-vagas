# Radar de Vagas

![CI](https://github.com/LucasSMFerreira/radar-vagas/actions/workflows/ci.yml/badge.svg)

Coleta vagas de back-end, automação e IA em fontes públicas, guarda tudo num PostgreSQL sem duplicar e, nas próximas etapas, vai ordenar as vagas pela aderência ao meu perfil com embeddings e enviar as melhores no Telegram.

> **Status:** em construção. A coleta e o armazenamento já funcionam; ranqueamento e alertas estão no roteiro abaixo.

## Como funciona

```
Remotive (API pública) ─┐
                        ├─► coletores ─► modelo Vaga (Pydantic) ─► PostgreSQL
Adzuna (API oficial) ───┘                 HTML limpo              sem duplicar (fonte + id)
```

1. **Coleta:** cada fonte tem um coletor próprio em `radar/coletores/`, que busca as vagas com `httpx` e converte para o modelo `Vaga`.
2. **Limpeza:** a descrição vem em HTML e é convertida em texto simples (`radar/texto.py`).
3. **Armazenamento:** `INSERT ... ON CONFLICT DO NOTHING` na chave `(fonte, id_externo)`. Rodar a coleta várias vezes não cria vagas repetidas, e o comando informa quantas eram novas.

## Fontes

- Vagas remotas: [Remotive](https://remotive.com), pela API pública oficial.
- Vagas no Brasil: [Jobs by Adzuna](https://www.adzuna.com.br), pela API oficial (precisa de `ADZUNA_APP_ID` e `ADZUNA_APP_KEY`).

## Rodar localmente

Requisitos: Python 3.12 e Docker.

```bash
cp .env.example .env                       # ajuste a senha e as chaves do Adzuna
docker compose up -d                       # PostgreSQL 17 com pgvector em 127.0.0.1:5433
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < sql/001_schema.sql

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m radar.cli coletar remotive
python -m radar.cli coletar adzuna
```

Cada comando mostra quantas vagas recebeu e quantas eram novas. Se rodar de novo em seguida, as vagas já salvas não se repetem.

## Testes

```bash
pytest -v -m "not integracao"   # unitários, com respostas das APIs gravadas em tests/fixtures
pytest -v                       # inclui os testes de integração (precisa do Postgres rodando)
```

O CI no GitHub Actions roda os testes unitários a cada push e pull request.

## Tecnologias

Python 3.12 · httpx · Pydantic · SQLAlchemy · PostgreSQL 17 + pgvector · Docker Compose · pytest · GitHub Actions

## Roteiro

- [x] Modelo `Vaga` e coletor do Remotive
- [x] Banco PostgreSQL com deduplicação
- [x] Coletor do Adzuna
- [ ] Embeddings das vagas e do meu perfil no pgvector
- [ ] Nota de aderência e ordenação das vagas
- [ ] Alerta diário no Telegram com as melhores
- [ ] Execução agendada, com novas tentativas e logs
