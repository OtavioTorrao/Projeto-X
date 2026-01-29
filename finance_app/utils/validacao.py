"""Validações de entrada."""
from __future__ import annotations

from datetime import date
from decimal import Decimal


def validate_non_empty(value: str, field_name: str) -> str:
    """Valida string não vazia."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} não pode ser vazio.")
    return value.strip()


def validate_positive(value: Decimal, field_name: str) -> Decimal:
    """Valida número positivo."""
    if value <= 0:
        raise ValueError(f"{field_name} deve ser positivo.")
    return value


def validate_date(value: date, field_name: str) -> date:
    """Valida data informada."""
    if not isinstance(value, date):
        raise ValueError(f"{field_name} deve ser uma data válida.")
    return value
