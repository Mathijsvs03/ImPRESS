import dash_bootstrap_components as dbc
from dash import html, dcc

def build_prompt_panel(keywords):
    key_dist_list = html.Div([
        html.Div([
            html.H5(kw),
            html.Div("Distribution graph", style={'height': '100px', 'background': '#829198'})
        ], className="mb-3")
        for kw in keywords
    ], style={'maxHeight': '40vh', 'overflowY': 'auto'})

    return dbc.Card([
        dbc.CardHeader("Prompt Configuration", className="bg-light"),
        dbc.CardBody([
            dbc.Label("Prompt"),
            dbc.Textarea(id="Prompt", placeholder="Enter prompt", style={'marginBottom': '1rem'}),

            dbc.Label("Negative Prompt"),
            dbc.Textarea(id="NegPrompt", placeholder="Enter negative prompt", style={'marginBottom': '1rem'}),

            dbc.Label("Guidance Scale"),
            dcc.RangeSlider(
                0, 50, 1, value=[5, 15], allowCross=False,
                marks={i: str(i) for i in range(0, 51, 10)},
                tooltip={"placement": "bottom", "always_visible": True},
                id="guidance-slider"
            ),

            dbc.Button("Generate Image", id="generate-image-button", color="primary", className="mt-3 me-2"),
            dbc.Button("Generate Prompt", id="generate-prompt-button", color="secondary", className="mt-3"),

            html.Hr(),
            html.H5("Keyword Distribution"),
            key_dist_list
        ])
    ], style={"height": "100%"}, className="flex-grow-1")
