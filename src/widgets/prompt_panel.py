import dash_bootstrap_components as dbc
from dash import html, dcc

def build_prompt_panel():
    return html.Div([
        dcc.Store(id="prompt-text-length", data=0),

        dbc.Card([
            dbc.CardBody([

                dbc.Row([
                    dbc.Col(dbc.Label("Generate an image:"), width=12),
                    dbc.Col(
                        dbc.Textarea(
                            id="Prompt",
                            placeholder="Describe the image you want to create...",
                            className="prompt-field",
                            style={"height": "150px", "width": "100%", "padding": "10px"}
                        ),
                        width=12
                    )
                ], className="mb-4"),

                html.Div([
                    html.H6("Generate Image", className="mb-2"),
                    dbc.Button(
                        [html.Span("🖼️", style={"marginRight": "5px"}), "Generate Image"],
                        id="generate-image-button",
                        color="primary",
                        className="w-100",
                    )
                ], className="mb-4"),

                html.Hr(className="my-4"),

                html.Div([
                    html.H6("Improve your prompt", className="mb-2"),
                    html.Div([
                        html.Div([
                            dbc.Label("Guidance Scale", html_for="guidance-slider"),
                            html.Span("(i)", id="guidance-tooltip-icon",
                                     style={"marginLeft": "6px", "cursor": "pointer"})
                        ]),
                        dcc.Slider(
                            id="guidance-slider",
                            min=1, max=5, step=1, value=3,
                            marks={i: str(i) for i in range(1, 6)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        dbc.Tooltip(
                            "Controls how much the model rewrites your prompt. "
                            "The higher the score the more the prompt will be changed.",
                            target="guidance-tooltip-icon",
                            placement="right"
                        )
                    ], className="mb-3"),
                    dbc.Button(
                        [html.Span("✨", style={"filter": "brightness(0) invert(1)",
                                                 "marginRight": "5px"}),
                         "Generate Prompt Suggestion"],
                        id="generate-prompt-button",
                        color="secondary",
                        className="w-100"
                    )
                ],
                id="prompt-tools-container",
                style={"display": "none"}),

                html.Div(build_prompt_modal(), className='modal-container')
            ])
        ], className="main-container")
    ])

def build_prompt_modal():
    return dbc.Modal([
        dbc.ModalHeader("Suggested Prompt"),
        dbc.ModalBody(id="llm-suggestion-modal-body"),
        dbc.ModalFooter([
            dbc.Button("Accept", id="accept-llm-suggestion", color="success", className="me-2"),
            dbc.Button("Decline", id="decline-llm-suggestion", color="secondary")
        ], id="llm-suggestion-modal-footer")
    ], id="llm-suggestion-modal", is_open=False)
