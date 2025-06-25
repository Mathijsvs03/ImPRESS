import dash_bootstrap_components as dbc
from dash import html

def build_history_panel():
    return dbc.Card(
        style={"height": "100%"},
        children=[
            dbc.CardBody(
            html.Div(
                id="history-wrapper", className="history-panel"
            ), style={"height": "100%"})
        ]
    )