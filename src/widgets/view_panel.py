import dash_bootstrap_components as dbc
from dash import html, dcc

def build_view_panel():
    return dbc.Card([
        dbc.CardHeader("Image View"),
        dbc.CardBody([
            dcc.Tabs(
                id="view-toggle",
                value="generated",
                children=[
                    dcc.Tab(label="Generated Image", value="generated"),
                    dcc.Tab(label="Clustered View", value="cluster")
                ],
                className="view-items"
            ),
            html.Div(
                id="main-view",
                className="view"
            )
        ])
    ], className="view-container")
