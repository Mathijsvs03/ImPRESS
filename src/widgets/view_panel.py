import dash_bootstrap_components as dbc
from dash import html, dcc

def build_view_panel():
    return dbc.Card([
        dbc.CardHeader("Image View"),
        dbc.CardBody([
            dcc.RadioItems(
                id="view-toggle",
                options=[
                    {"label": "Generated Image", "value": "generated"},
                    {"label": "Clustered View", "value": "cluster"},
                ],
                value="generated",
                labelStyle={"display": "inline-block", "marginRight": "20px"},
                style={"marginBottom": "10px"}
            ),
            html.Div(id="main-view", style={'height': '100%', 'width': '100%', 'padding': '10px'})
        ])
    ])