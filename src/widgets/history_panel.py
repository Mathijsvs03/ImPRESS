import dash_bootstrap_components as dbc
from dash import html, dcc

def build_history_panel():
    return dbc.Card([
        dbc.CardBody(
           html.Div(id="history-wrapper")
        )
    ])