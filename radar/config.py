import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://radar:radar@127.0.0.1:5433/radar"
)

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
PALAVRAS_CHAVE = os.getenv("PALAVRAS_CHAVE", "python java backend fastapi django")