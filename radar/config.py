import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://radar:radar@127.0.0.1:5433/radar"
)