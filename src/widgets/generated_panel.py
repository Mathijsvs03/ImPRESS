import dash_bootstrap_components as dbc
from dash import html, dcc

def build_generated_panel():
    return dbc.Card([
        dbc.CardBody(
            dcc.Loading(
                html.Img(id="gen-image", className="gen-image"),
                type="circle"
            )
        )
    ])