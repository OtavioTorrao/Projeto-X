"""Pacote de componentes do Dash."""
from finance_app.components.dashboard import layout as dashboard_layout
from finance_app.components.metas import layout as metas_layout
from finance_app.components.portfolio import layout as portfolio_layout
from finance_app.components.transacoes import layout as transacoes_layout
from finance_app.components.transacoes import register_callbacks as transacoes_callbacks

__all__ = [
    "dashboard_layout",
    "metas_layout",
    "portfolio_layout",
    "transacoes_layout",
    "transacoes_callbacks",
]
