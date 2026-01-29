"""Integrações com provedores de mercado."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import Decimal

import yfinance as yf

from finance_app.api.cache import get_cached_price, store_price


def fetch_price_yfinance(ticker: str) -> Decimal:
    """Busca preço atual via yfinance."""
    ticker_data = yf.Ticker(ticker)
    price = ticker_data.fast_info.get("last_price")
    if price is None:
        raise ValueError("Preço não disponível para o ticker informado.")
    return Decimal(str(price))


def get_latest_price(
    connection: sqlite3.Connection,
    ticker: str,
    now: datetime,
    ttl_seconds: int,
) -> Decimal:
    """Retorna preço atual com cache e fallback no provedor."""
    cached = get_cached_price(connection, ticker, ttl_seconds, now)
    if cached:
        return cached.preco

    price = fetch_price_yfinance(ticker)
    store_price(connection, ticker, price, now)
    return price
