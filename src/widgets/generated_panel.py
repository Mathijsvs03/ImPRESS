# src/widgets/generated_panel.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def build_image_download_button(img_src):
    return html.Div([
        html.Img(
            src=img_src,
            className="gen-image",
            alt="Generated image",
            style={"width": "100%", "height": "100%", "objectFit": "contain", "borderRadius": "4px"}
        ),
        dbc.Button(
            html.I(className="bi bi-download"),
            id="download-image-button",
            className="download-button",
            color="light",
            size="sm",
            n_clicks=0,
            title="Download image"
        ),
        dcc.Download(id="download-image"),
    ], style={"position": "relative", "display": "flex", "alignItems": "center", "justifyContent": "center", "height": "100%", "width": "100%"})


def build_generated_panel():
    return dbc.Card([
        dbc.CardBody(
            dbc.Row([
                dbc.Col(
                    dcc.Loading(
                        html.Div(
                            "Please generate an image to begin inspecting it.",
                            id="generated-content",
                            className="generated-container"
                        ), style={"height": "100%", "width": "100%"},
                        type="default"
                    ),
                    width=6,
                    style={"textAlign": "center", "height": "100%", "display": "flex", "alignItems": "center", "justifyContent": "center"}
                ),

                dbc.Col(
                    html.Div(
                        [
                            dcc.Clipboard(
                                target_id="selected-prompt",
                                title="Copy to clipboard",
                                style={
                                    "position": "absolute",
                                    "top": "10px",
                                    "right": "10px",
                                    "zIndex": "10",
                                    "cursor": "pointer"
                                }
                            ),
                            html.Div(
                                html.P(id="selected-prompt", className="prompt-text"),
                                className="prompt-box"
                            )
                        ],
                        className="prompt-wrapper",
                        style={"height": "100%", "overflowY": "auto"}
                    ),
                    width=6,
                    style={"borderLeft": "2px solid #ccc", "paddingLeft": "20px"}
                )
            ], style={"height": "100%"})
        , style={"height": "100%"})
    ], style={"height": "100%"})
