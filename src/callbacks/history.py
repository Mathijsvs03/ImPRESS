from dash import html, callback, Output, Input, ALL, no_update, ctx, State
import dash_bootstrap_components as dbc

@callback(
    Output("history-wrapper", "children"),
    Input("history-store", "data"),
    Input("selected-image", "data"),
)
def update_history_display(history, selected_src):
    if not history:
        return html.Div([
            html.P("Your generated images will appear here.\n")
        ], id="image-history", className="history-panel")

    cards = []
    for item in reversed(history):
        is_selected = selected_src and item["id"] == selected_src.get("id")
        cards.append(
            dbc.Card(
                [
                    dbc.Button(
                        html.Img(src=item["src"], className="history-image"),
                        id={'type': 'thumb', 'index': item["id"]},
                        n_clicks=0,
                        className="hist-entry-button"
                    ),
                    dbc.Tooltip(
                        item["prompt"],
                        target={'type': 'thumb', 'index': item["id"]},
                        placement="bottom",
                        style={"whiteSpace": "normal", "textAlign": "left"}
                    )
                ],
                id={'type': 'card', 'index': item["id"]},
                className=f"history-entry{' selected-history-entry' if is_selected else ''}"
            )
        )

    return html.Div(cards, id="image-history", className="history-panel")
