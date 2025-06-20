from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
from src.llm_utils import get_llm_suggestions

@callback(
    Output("llm-suggestion-modal", "is_open", allow_duplicate=True),
    Output("llm-suggestion-modal-body", "children"),
    Input("generate-prompt-button", "n_clicks"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def open_modal_immediately(n_clicks, prompt_value):
    if not n_clicks or not prompt_value:
        raise PreventUpdate
    return True, "⏳ Generating prompt suggestion..."

@callback(
    Output("llm-suggestion-modal-body", "children", allow_duplicate=True),
    Input("llm-suggestion-modal", "is_open"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def update_llm_text(is_open, prompt_value):
    if not is_open or not prompt_value:
        raise PreventUpdate
    try:
        suggestion = get_llm_suggestions(prompt_value)
        return suggestion
    except Exception as e:
        return f"❌ Error: {str(e)}"

@callback(
    Output("llm-suggestion-modal", "is_open"),
    Output("Prompt", "value"),
    Input("accept-llm-suggestion", "n_clicks"),
    Input("decline-llm-suggestion", "n_clicks"),
    State("llm-suggestion-modal-body", "children"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def handle_modal_action(accept_click, decline_click, suggestion_text, current_prompt):
    triggered = ctx.triggered_id
    if triggered == "accept-llm-suggestion":
        return False, suggestion_text
    elif triggered == "decline-llm-suggestion":
        return False, current_prompt
    raise PreventUpdate
