import dash_bootstrap_components as dbc
from dash import html

def build_keyword_panel(keywords):
    return dbc.Card([
        dbc.CardHeader("Clustered View"),
        dbc.CardBody([
            html.P("This panel is shown in clustered view."),
            html.H5("Keyword Distribution"),
            html.Ul([html.Li(kw) for kw in keywords])
        ])
    ])
