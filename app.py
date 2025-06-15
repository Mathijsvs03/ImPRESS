from dash import Dash, html, dcc, callback, Output, Input, State, ctx
import dash
import base64
from io import BytesIO
import dash_split_pane
import os
from Models.generator import generate_image

app = Dash(suppress_callback_exceptions=True)

def load_template_images():
    folder = "assets/templates"
    template_history = []
    if not os.path.exists(folder):
        return []

    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder, filename)
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                src = f"data:image/png;base64,{encoded}"
                template_history.append({"src": src, "prompt": f"Template: {filename}"})
    return template_history

initial_history = load_template_images()

keywords = ['Keyword 1', 'Keyword 2', 'Keyword 3']
key_dist_list = html.Div([
    html.Div([
        html.H4(kw),
        html.Div("Distribution graph", style={'height': '100px', 'background': '#829198'})
    ], style={'padding': '10px', 'borderBottom': '1px solid #ccc'})
    for kw in keywords
], style={'height': '100%', 'overflowY': 'scroll', 'padding': '10px'})

app.layout = html.Div([
    dcc.Store(id="history-store", data=initial_history),
    dcc.Store(id="selected-image", data=initial_history[0]["src"] if initial_history else ""),
    html.H1('ImPress', style={'textAlign': 'left', 'margin': '10px'}),

    dash_split_pane.DashSplitPane(
        split="vertical", size="23%",
        style={'borderTop': '2px solid #000', 'width': '100%'},
        children=[

            dash_split_pane.DashSplitPane(
                split="horizontal", size="31%", style={'width': '100%'},
                children=[
                    html.Div([
                        dcc.Textarea(id="Prompt", placeholder="Enter prompt", style={'height': '30%', 'width': '100%'}),
                        dcc.Textarea(id="NegPrompt", placeholder="Negative prompt", style={'height': '15%', 'width': '100%'}),
                        html.Div("Guidance Scale", style={"marginTop": '10px'}),
                        dcc.RangeSlider(0, 50, 1, value=[5, 15], allowCross=False,
                                        marks={i: str(i) for i in range(0, 51, 10)},
                                        tooltip={"placement": "bottom", "always_visible": True}),
                        html.Button("Generate image", id="generate-button",
                                    style={'marginTop': '10px', 'fontSize': '24px'})
                    ], style={'padding': '3px', 'paddingRight': '12px'}),

                    html.Div([
                        html.Button("Generate prompt", style={'marginTop': '10px', 'fontSize': '24px'}),
                        key_dist_list
                    ])
                ]
            ),

            dash_split_pane.DashSplitPane(
                split="horizontal", size="70%",
                children=[
                    html.Div([
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
                        html.Div(id="main-view", style={'height': '100%', 'width': '100%', 'padding': '20px'})
                    ]),

                    html.Div(id="image-history", style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'overflowX': 'auto',
                        'padding': '10px',
                        'height': '100%',
                        'whiteSpace': 'nowrap',
                        'border': '1px solid #aaa'
                    })
                ]
            )
        ]
    )
], style={'height': '100vh'})


from dash import ALL

@callback(
    Output("history-store", "data"),
    Output("selected-image", "data"),
    Input("generate-button", "n_clicks"),
    Input({'type': 'thumb', 'index': ALL}, 'n_clicks'),
    State("Prompt", "value"),
    State("NegPrompt", "value"),
    State("history-store", "data"),
    prevent_initial_call=True
)
def handle_image_selection_or_generation(gen_clicks, thumb_clicks, prompt, neg_prompt, history):
    triggered_id = ctx.triggered_id

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "thumb":
        index = triggered_id["index"]
        selected = list(reversed(history))[index]
        return dash.no_update, selected["src"]

    if not prompt:
        return dash.no_update, dash.no_update

    img = generate_image(prompt, neg_prompt or "")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    img_str = f"data:image/png;base64,{img_base64}"

    history.append({"src": img_str, "prompt": prompt})
    return history, img_str

@callback(
    Output("image-history", "children"),
    Input("history-store", "data")
)
def update_history_display(history):
    return [
        html.Div([
            html.Button([
                html.Img(src=item["src"], style={'height': '150px'}),
                html.H4(item["prompt"])
            ], id={'type': 'thumb', 'index': i}, n_clicks=0, style={'border': 'none', 'background': 'none'})
        ], style={
            'minWidth': '200px', 'marginRight': '10px',
            'padding': '10px', 'border': '1px solid #ccc',
            'borderRadius': '5px', 'backgroundColor': '#f5f5f5'
        })
        for i, item in enumerate(reversed(history))
    ]


@callback(
    Output("main-view", "children"),
    Input("view-toggle", "value"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_main_view(view_mode, selected_image):
    if view_mode == "cluster":
        return html.Div([
            html.H3("Clustered Dataset View"),
            html.Div("This is where clustered images will appear.", style={
                'height': '500px',
                'backgroundColor': '#eee',
                'border': '2px dashed #aaa',
                'textAlign': 'center',
                'lineHeight': '500px',
                'color': '#666'
            })
        ])
    else:
        return html.Div([
            html.H3("Generated Image:"),
            dcc.Loading(
                html.Img(src=selected_image, id="generated-image", style={'width': '100%', 'maxHeight': '600px'}),
                type="circle"
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
