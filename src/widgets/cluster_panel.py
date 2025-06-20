import dash_bootstrap_components as dbc
from dash import html, dcc

def build_cluster_panel():
    return dbc.Card([
        dbc.CardHeader("Clustered Dataset View"),
        dbc.CardBody(
            html.Div("This is where clustered images will appear.",
                        className="cluster-field")
        )
    ])