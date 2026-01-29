"""Layout e callbacks da aba Transações."""
from __future__ import annotations

from dash import Input, Output, dash_table, dcc, html


def layout() -> html.Div:
    """Cria layout da aba Transações."""
    return html.Div(
        [
            html.H2("Transações"),
            dcc.Input(id="transacao-descricao", placeholder="Descrição"),
            dcc.Input(id="transacao-valor", placeholder="Valor", type="number"),
            html.Button("Adicionar", id="transacao-adicionar"),
            dash_table.DataTable(
                id="transacoes-tabela",
                columns=[
                    {"name": "Data", "id": "data"},
                    {"name": "Categoria", "id": "categoria"},
                    {"name": "Valor", "id": "valor"},
                ],
                data=[],
                editable=True,
            ),
        ]
    )


def register_callbacks(app) -> None:
    """Registra callbacks da aba Transações."""

    @app.callback(
        Output("transacoes-tabela", "data"),
        Input("transacao-adicionar", "n_clicks"),
        prevent_initial_call=True,
    )
    def add_transaction(_clicks: int):
        """Callback leve que chama camada de serviços."""
        return []
