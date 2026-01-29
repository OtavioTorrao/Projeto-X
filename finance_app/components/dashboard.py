"""Layout da aba Resumo."""
from __future__ import annotations

from dash import dcc, html

from finance_app.components.charts import line_balance, pie_expenses


def layout() -> html.Div:
    """Cria layout da aba Resumo."""
    pie_chart = pie_expenses(["Moradia", "Alimentação"], [1200, 800])
    line_chart = line_balance(["2024-01", "2024-02"], [1000, 1500])

    return html.Div(
        [
            html.H2("Resumo"),
            html.Div(
                [
                    html.Div("Receitas: R$ 0,00", className="kpi"),
                    html.Div("Despesas: R$ 0,00", className="kpi"),
                    html.Div("Saldo: R$ 0,00", className="kpi"),
                ],
                className="kpi-grid",
            ),
            html.Div(
                [
                    dcc.Graph(figure=pie_chart),
                    dcc.Graph(figure=line_chart),
                ],
                className="charts-grid",
            ),
        ]
    )
