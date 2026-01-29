"""Ponto de entrada do Dash."""
from __future__ import annotations

from dash import Dash, Input, Output, dcc, html

from finance_app import config
from finance_app.components import (
    dashboard_layout,
    metas_layout,
    portfolio_layout,
    transacoes_callbacks,
    transacoes_layout,
)

app = Dash(__name__, title=config.DASH_TITLE)

app.layout = html.Div(
    [
        html.H1("Finance App"),
        dcc.Tabs(
            id="tabs",
            value="resumo",
            children=[
                dcc.Tab(label="Resumo", value="resumo"),
                dcc.Tab(label="Transações", value="transacoes"),
                dcc.Tab(label="Portfólio", value="portfolio"),
                dcc.Tab(label="Metas", value="metas"),
            ],
        ),
        html.Div(id="tab-content"),
    ]
)


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab: str):
    """Roteia layout das abas."""
    if tab == "transacoes":
        return transacoes_layout()
    if tab == "portfolio":
        return portfolio_layout()
    if tab == "metas":
        return metas_layout()
    return dashboard_layout()


transacoes_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
