# src/widgets/generated_panel.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def build_generated_panel():
    return dbc.Card(
        [
            dbc.CardBody(
                dbc.Row(
                    [

                        dbc.Col(
                            dcc.Loading(
                                html.Div(
                                    "Please generate an image to begin inspecting it.",
                                    id="generated-content",
                                    className="generated-container"
                                ),
                                type="default"
                            ),
                            width=6,
                            style={"textAlign": "center", "height": "100%"}
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
                    ],
                    style={"height": "100%"}
                ),
                style={"height": "550px"}
            )
        ],
        style={"height": "550px"}
    )
