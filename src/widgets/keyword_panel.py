import dash_bootstrap_components as dbc
from dash import html

def build_keyword_content(keywords=None):
    if not keywords:
        return html.P("Make a selection on the scatterplot to generate style keywords.")

    return html.Div([
        html.H5("Keyword Distribution"),
        html.Ul([html.Li(kw) for kw in keywords])
    ])


def build_keyword_panel():
    return dbc.Card([
        dbc.CardBody([
            html.Div(id='keyword-content', children=build_keyword_content())
        ])
    ])