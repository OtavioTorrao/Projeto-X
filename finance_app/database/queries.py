"""Consultas SQLite usadas pela aplicação."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import Decimal
from typing import Iterable, Optional

from finance_app.database.models import Goal, PriceHistory, Transaction


def create_tables(connection: sqlite3.Connection) -> None:
    """Cria tabelas e índices do banco."""
    statements = [
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            recorrente INTEGER NOT NULL,
            criado_em TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            nome TEXT NOT NULL,
            tipo_ativo TEXT NOT NULL,
            quantidade REAL NOT NULL,
            preco_medio REAL NOT NULL,
            data_compra TEXT NOT NULL,
            observacoes TEXT NOT NULL,
            criado_em TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS historico_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            preco REAL NOT NULL,
            data_hora TEXT NOT NULL,
            UNIQUE(ticker, data_hora)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor_alvo REAL NOT NULL,
            valor_atual REAL NOT NULL,
            prazo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            ativa INTEGER NOT NULL,
            criado_em TEXT NOT NULL
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_categoria ON transacoes(categoria)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_historico_precos_ticker_data
        ON historico_precos(ticker, data_hora)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_metas_ativa ON metas(ativa)
        """,
    ]
    for statement in statements:
        connection.execute(statement)
    connection.commit()


def insert_transaction(connection: sqlite3.Connection, transaction: Transaction) -> int:
    """Insere uma transação e retorna o id gerado."""
    cursor = connection.execute(
        """
        INSERT INTO transacoes (data, tipo, categoria, descricao, valor, recorrente, criado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            transaction.data.isoformat(),
            transaction.tipo,
            transaction.categoria,
            transaction.descricao,
            float(transaction.valor),
            int(transaction.recorrente),
            transaction.criado_em.isoformat(),
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def list_recent_transactions(
    connection: sqlite3.Connection,
    limit: int = 5,
) -> list[Transaction]:
    """Lista as últimas transações."""
    cursor = connection.execute(
        """
        SELECT id, data, tipo, categoria, descricao, valor, recorrente, criado_em
        FROM transacoes
        ORDER BY data DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    return [
        Transaction(
            id=row["id"],
            data=datetime.fromisoformat(row["data"]).date(),
            tipo=row["tipo"],
            categoria=row["categoria"],
            descricao=row["descricao"],
            valor=Decimal(str(row["valor"])),
            recorrente=bool(row["recorrente"]),
            criado_em=datetime.fromisoformat(row["criado_em"]),
        )
        for row in rows
    ]


def upsert_price_history(
    connection: sqlite3.Connection,
    history: PriceHistory,
) -> None:
    """Registra histórico de preço para um ticker."""
    connection.execute(
        """
        INSERT INTO historico_precos (ticker, preco, data_hora)
        VALUES (?, ?, ?)
        ON CONFLICT(ticker, data_hora) DO UPDATE SET preco = excluded.preco
        """,
        (history.ticker, float(history.preco), history.data_hora.isoformat()),
    )
    connection.commit()


def get_latest_price(
    connection: sqlite3.Connection,
    ticker: str,
) -> Optional[PriceHistory]:
    """Retorna o preço mais recente para um ticker."""
    cursor = connection.execute(
        """
        SELECT id, ticker, preco, data_hora
        FROM historico_precos
        WHERE ticker = ?
        ORDER BY data_hora DESC
        LIMIT 1
        """,
        (ticker,),
    )
    row = cursor.fetchone()
    if not row:
        return None
    return PriceHistory(
        id=row["id"],
        ticker=row["ticker"],
        preco=Decimal(str(row["preco"])),
        data_hora=datetime.fromisoformat(row["data_hora"]),
    )


def list_active_goals(connection: sqlite3.Connection) -> list[Goal]:
    """Lista metas ativas."""
    cursor = connection.execute(
        """
        SELECT id, descricao, valor_alvo, valor_atual, prazo, categoria, ativa, criado_em
        FROM metas
        WHERE ativa = 1
        ORDER BY prazo ASC
        """
    )
    rows = cursor.fetchall()
    return [
        Goal(
            id=row["id"],
            descricao=row["descricao"],
            valor_alvo=Decimal(str(row["valor_alvo"])),
            valor_atual=Decimal(str(row["valor_atual"])),
            prazo=datetime.fromisoformat(row["prazo"]).date(),
            categoria=row["categoria"],
            ativa=bool(row["ativa"]),
            criado_em=datetime.fromisoformat(row["criado_em"]),
        )
        for row in rows
    ]
