"""Layout da aba Portfólio."""
from __future__ import annotations

from dash import dash_table, html


def layout() -> html.Div:
    """Cria layout da aba Portfólio."""
    return html.Div(
        [
            html.H2("Portfólio"),
            html.Button("Atualizar preços", id="portfolio-atualizar"),
            dash_table.DataTable(
                id="portfolio-tabela",
                columns=[
                    {"name": "Ticker", "id": "ticker"},
                    {"name": "Quantidade", "id": "quantidade"},
                    {"name": "Preço Médio", "id": "preco_medio"},
                ],
                data=[],
            ),
        ]
    )
