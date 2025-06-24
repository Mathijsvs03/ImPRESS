import dash
from dash import callback, Input, Output, State, html

@callback(
    Output("is-generating-keywords", "data", allow_duplicate=True),
    Input("generate-keywords-button", "n_clicks"),
    State("generate-keywords-button",  "disabled"),
    prevent_initial_call=True
)
def start_generating_keywords(n_clicks, is_disabled):
    if not is_disabled:
        return True
    return dash.no_update

@callback(
    Output("is-generating-keywords", "data", allow_duplicate=True),
    Input("keyword-content", "children"),
    prevent_initial_call=True
)
def stop_generating_keywords(_children):
    return False

@callback(
    Output("generate-keywords-button", "disabled"),
    Output("generate-keywords-button", "children"),
    Input("is-generating-keywords", "data"),
    Input('stored-selection', 'data'),
    State("generate-keywords-button", "children")
)
def toggle_keywords_button(is_generating, stored_data, current_children):
    if is_generating:
        return True, [
            html.Span(
                className="spinner-border spinner-border-sm",
                role="status",
                style={"marginRight": "5px"}
            ),
            "Generating…"
        ]

    if not stored_data or "points" not in stored_data or len(stored_data["points"]) == 0:
        return True, [html.Span("🔄", style={"marginRight":"5px"}), "Generate Keywords"]

    return False, [html.Span("🔄", style={"marginRight":"5px"}), "Generate Keywords"]
