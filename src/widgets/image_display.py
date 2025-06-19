import dash_bootstrap_components as dbc
from dash import html


def create_image_display():
    return dbc.Card([
        dbc.CardBody(
            html.Div(id="gen-image-container", className="image-field")
        )
    ])

