"""Cálculos financeiros básicos."""
from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from finance_app.database.models import Transaction


def total_by_type(transactions: Iterable[Transaction], tipo: str) -> Decimal:
    """Soma valores por tipo de transação."""
    total = Decimal("0")
    for transaction in transactions:
        if transaction.tipo == tipo:
            total += transaction.valor
    return total
