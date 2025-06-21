import dash_bootstrap_components as dbc
from dash import html, dcc

def build_prompt_panel():
    return html.Div([
        dbc.Card([
            dbc.CardHeader("Prompt Configuration", className="bg-light"),
            dbc.CardBody([
                dbc.Label("Prompt"),
                dbc.Textarea(id="Prompt", placeholder="Enter prompt", className="promp-field", style={"height": "150px", "width": "100%", "padding": "10px"}),

                dbc.Label("Negative Prompt"),
                dbc.Textarea(id="NegPrompt", placeholder="Enter negative prompt", className="prompt-field"),

                dbc.Label("Guidance Scale"),
                dcc.RangeSlider(
                    0, 50, 1, value=[5, 15], allowCross=False,
                    marks={i: str(i) for i in range(0, 51, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    id="guidance-slider"
                ),

                dbc.Button("Generate Image", id="generate-image-button", color="primary", className="mt-3 me-2"),
                dbc.Button([
                                html.Span("✨", style={"filter": "brightness(0) invert(1)", "marginRight": "5px"}),
                                "Generate Prompt"
                            ], id="generate-prompt-button", color="secondary", className="mt-3"),

                html.Hr(),

                html.Div(build_prompt_modal(), className='modal-container')
            ])
        ], className="flex-grow-1 main-container"),
    ])

def build_prompt_modal():
    return dbc.Modal([
        dbc.ModalHeader("Suggested Prompt"),
        dbc.ModalBody(id="llm-suggestion-modal-body"),
        dbc.ModalFooter([
            dbc.Button("Accept", id="accept-llm-suggestion", color="success", className="me-2"),
            dbc.Button("Decline", id="decline-llm-suggestion", color="secondary")
        ])
    ], id="llm-suggestion-modal", is_open=False)

