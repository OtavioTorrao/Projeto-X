"""Modelos de dados usados pela aplicação."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Transaction:
    """Representa uma transação financeira."""
    id: Optional[int]
    data: date
    tipo: str
    categoria: str
    descricao: str
    valor: Decimal
    recorrente: bool
    criado_em: datetime


@dataclass(frozen=True)
class Asset:
    """Representa um ativo do portfólio."""
    id: Optional[int]
    ticker: str
    nome: str
    tipo_ativo: str
    quantidade: Decimal
    preco_medio: Decimal
    data_compra: date
    observacoes: str
    criado_em: datetime


@dataclass(frozen=True)
class PriceHistory:
    """Representa um preço de ativo em determinada data/hora."""
    id: Optional[int]
    ticker: str
    preco: Decimal
    data_hora: datetime


@dataclass(frozen=True)
class Goal:
    """Representa uma meta financeira."""
    id: Optional[int]
    descricao: str
    valor_alvo: Decimal
    valor_atual: Decimal
    prazo: date
    categoria: str
    ativa: bool
    criado_em: datetime
