import dash_bootstrap_components as dbc
from dash import html, dcc

def build_history_panel():
    return dbc.Card([
        dbc.CardHeader("Image History"),
        dbc.CardBody(
            html.Div(id="image-history", className="history-panel")
        )
    ])