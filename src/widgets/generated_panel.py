import dash_bootstrap_components as dbc
from dash import html, dcc

def build_generated_panel():
    return dbc.Card([
        dbc.CardBody(
            dbc.Row([
                dbc.Col(
                    dcc.Loading(
                        html.Img(id="gen-image", className="gen-image",
                                alt="Selected image"),
                        type="circle"
                    ), width="auto"
                ),
                dbc.Col(
                    html.P("Selected image generation prompt", id="selected-prompt")
                )
            ])
        )
    ])