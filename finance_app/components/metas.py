"""Layout da aba Metas."""
from __future__ import annotations

from dash import dash_table, html


def layout() -> html.Div:
    """Cria layout da aba Metas."""
    return html.Div(
        [
            html.H2("Metas"),
            dash_table.DataTable(
                id="metas-tabela",
                columns=[
                    {"name": "Descrição", "id": "descricao"},
                    {"name": "Valor Alvo", "id": "valor_alvo"},
                    {"name": "Valor Atual", "id": "valor_atual"},
                ],
                data=[],
            ),
        ]
    )
