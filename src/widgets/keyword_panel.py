import dash_bootstrap_components as dbc
from dash import html, dcc

def build_keyword_content(keywords=None):
    if not keywords:
        return html.P("Make a selection on the scatterplot to generate style keywords.")
    return html.Div([
        html.H5("Keyword Distribution"),
        html.Ul([html.Li(kw) for kw in keywords])
    ])

def build_keyword_panel():
    return html.Div([

        dcc.Store(id="is-generating-keywords", data=False),

        dbc.Card([
            dbc.CardBody([
                dcc.Loading(
                    id="loading-keywords",
                    type="circle",
                    children=html.Div(
                        id='keyword-content',
                        children=build_keyword_content()
                    )
                ),
                html.Hr(className="my-4"),
                dbc.Button(
                    [html.Span("🔄", style={"marginRight": "5px"}), "Generate Keywords"],
                    id="generate-keywords-button",
                    color="primary",
                    disabled=True,
                    className="w-100"
                ),
            ])
        ])
    ])
