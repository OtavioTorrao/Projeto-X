"""Gráficos reutilizáveis do Dash."""
from __future__ import annotations

import plotly.express as px


def pie_expenses(labels: list[str], values: list[float]):
    """Cria gráfico de pizza de despesas."""
    return px.pie(names=labels, values=values, title="Despesas por categoria")


def line_balance(dates: list[str], values: list[float]):
    """Cria gráfico de linha de evolução."""
    return px.line(x=dates, y=values, title="Evolução do saldo")
