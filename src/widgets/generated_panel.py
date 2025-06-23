import dash_bootstrap_components as dbc
from dash import html

def build_generated_panel():
    return dbc.Card([
        dbc.CardBody(
            dbc.Row([
                dbc.Col(
                    html.Img(id="gen-image", className="gen-image",
                                alt="Selected image"),
                    width="auto"
                ),
                dbc.Col(
                    html.P("Selected image generation prompt", id="selected-prompt")
                )
            ])
        )
    ])