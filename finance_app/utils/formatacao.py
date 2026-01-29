"""Funções de formatação."""
from __future__ import annotations

from decimal import Decimal


def format_currency(value: Decimal) -> str:
    """Formata valor como moeda."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
