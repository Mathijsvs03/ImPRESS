import dash_bootstrap_components as dbc
from dash import html, dcc

def keyword_item(keyword, i):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col(
                    html.P(keyword, id={'type': 'keyword', 'index': i})
                ),
                dbc.Col(
                    dcc.Slider(
                        id={'type': 'keyword-slider', 'index': i},
                        min=1, max=3, step=1, value=2,
                        marks={1: "Add inverse", 2: "Nothing", 3: "Add keyword"},
                        className="keyword-slider", included=False
                    )
                )
            ], align="center")
        )
    )


def build_keyword_content(keywords=None):
    if not keywords:
        return html.P("Make a selection on the scatterplot to generate style keywords.")
    return html.Div([
        html.H5("Keyword Distribution"),
        html.Div([keyword_item(kw, i) for i, kw in enumerate(keywords)], id="keyword-list",
                 className="keyword-list")
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
                    style={"marginBottom": "10px"},
                    className="w-100"
                ),
                dbc.Button(
                    [html.Span("✨", style={"marginRight": "5px"}), "Generate Prompt from Keywords"],
                    id="generate-prompt-button-keywords",
                    color="primary",
                    style={"display": "none"},
                    className="w-100"
                ),

                html.Div(build_prompt_from_keywords_modal(), className='modal-container')
            ])
        ])
    ])

def build_prompt_from_keywords_modal():
    return dbc.Modal([
        dbc.ModalHeader("Suggested Prompt from Keywords"),
        dbc.ModalBody(id="keywords-suggestion-modal-body"),
        dbc.ModalFooter([
            dbc.Button("Accept", id="accept-keywords-suggestion", color="success", className="me-2"),
            dbc.Button("Decline", id="decline-keywords-suggestion", color="secondary")
        ])
    ], id="keywords-suggestion-modal", is_open=False)
