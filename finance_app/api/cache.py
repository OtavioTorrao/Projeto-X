"""Cache baseado na tabela historico_precos."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from finance_app.database.models import PriceHistory
from finance_app.database.queries import get_latest_price, upsert_price_history


def is_cache_fresh(last_updated: datetime, ttl_seconds: int, now: datetime) -> bool:
    """Indica se o cache ainda está válido."""
    return now - last_updated <= timedelta(seconds=ttl_seconds)


def get_cached_price(
    connection: sqlite3.Connection,
    ticker: str,
    ttl_seconds: int,
    now: datetime,
) -> Optional[PriceHistory]:
    """Retorna preço em cache se estiver válido."""
    cached = get_latest_price(connection, ticker)
    if not cached:
        return None
    if is_cache_fresh(cached.data_hora, ttl_seconds, now):
        return cached
    return None


def store_price(
    connection: sqlite3.Connection,
    ticker: str,
    price: Decimal,
    now: datetime,
) -> None:
    """Registra preço no cache persistente."""
    history = PriceHistory(id=None, ticker=ticker, preco=price, data_hora=now)
    upsert_price_history(connection, history)
