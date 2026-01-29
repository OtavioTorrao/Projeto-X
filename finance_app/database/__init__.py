"""Conexões e helpers para o banco de dados."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Cria conexão com SQLite configurada."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def execute_script(connection: sqlite3.Connection, statements: Iterable[str]) -> None:
    """Executa múltiplos statements SQL em sequência."""
    for statement in statements:
        connection.execute(statement)
    connection.commit()
