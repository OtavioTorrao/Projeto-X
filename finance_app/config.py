"""Configurações centrais da aplicação."""
from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "financas.db"
CACHE_TTL_SECONDS = 60 * 30  # 30 minutos

DASH_TITLE = "Finance App"
