from dash import callback, Input, Output, State, ctx, html

@callback(
    Output("is-generating", "data", allow_duplicate=True),
    Input("generate-image-button", "n_clicks"),
    State("Prompt",           "value"),
    prevent_initial_call=True
)
def start_generating(n, prompt_text):
    return bool(prompt_text and prompt_text.strip())

@callback(
    Output("is-generating", "data", allow_duplicate=True),
    Input("history-store",        "data"),
    prevent_initial_call=True
)
def stop_generating(history):
    return False

@callback(
    Output("generate-image-button", "disabled"),
    Output("generate-image-button", "children"),
    Input("is-generating", "data"),
    State("generate-image-button", "children")
)
def toggle_button(is_generating, current_children):
    if is_generating:
        return True, [
            html.Span(
                className="spinner-border spinner-border-sm",
                role="status",
                style={"marginRight": "5px"}
            ),
            "Generating…"
        ]
    return False, [html.Span("🖼️", style={"marginRight": "5px"}), "Generate Image"]
