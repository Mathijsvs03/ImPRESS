import threading
from dash import Input, Output, State, callback, ctx, ALL
from dash.exceptions import PreventUpdate
from src.llm_utils import get_llm_suggestions

llm_suggestion_lock = threading.Lock()


# Callbacks for normal guidance level-based prompt suggestions
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
    State("guidance-slider", "value"),
    prevent_initial_call=True
)
def update_llm_text(is_open, prompt_value, guidance_level):
    if not is_open or not prompt_value:
        raise PreventUpdate

    guidance_prompt_levels = {
        1: "Make a very small improvement to the prompt. Keep it mostly unchanged.",
        2: "Make minor enhancements to improve clarity and creativity.",
        3: "Refactor the prompt moderately for better structure and more impact.",
        4: "Significantly improve the prompt while preserving its core idea.",
        5: "Completely rewrite the prompt to maximize creativity and effectiveness."
    }
    instruction = guidance_prompt_levels.get(guidance_level, "Improve this prompt.")

    try:
        with llm_suggestion_lock:
            suggestion = get_llm_suggestions(
                prompt_value,
                improvement_instruction=instruction
            )
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

# Callbacks for keyword-based prompt suggestions
@callback(
    Output("keywords-suggestion-modal", "is_open", allow_duplicate=True),
    Output("keywords-suggestion-modal-body", "children"),
    Input("generate-prompt-button-keywords", "n_clicks"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def open_modal_keywords_immediately(n_clicks, prompt_value):
    if not n_clicks or not prompt_value:
        raise PreventUpdate
    return True, "⏳ Generating prompt suggestion..."

@callback(
    Output("keywords-suggestion-modal-body", "children", allow_duplicate=True),
    Input("keywords-suggestion-modal", "is_open"),
    State("Prompt", "value"),
    State({"type": "keyword", "index": ALL}, "children"),
    State({"type": "keyword-slider", "index": ALL}, "value"),
    prevent_initial_call=True
)
def update_llm_text_keywords(is_open, prompt_value, keywords, selection):
    if not is_open or not prompt_value:
        raise PreventUpdate

    negatives = [keywords[i] for i, s in enumerate(selection) if s == 1]
    positives = [keywords[i] for i, s in enumerate(selection) if s == 3]
    neg_instruct = f"Incorporate the opposite of the following keywords: {' '.join(negatives)}.\n" if negatives else ""
    pos_instruct = f"Change the prompt by incorporating the following keywords: {' '.join(positives)}.\n" if positives else ""

    instruction = pos_instruct + neg_instruct + "Stay close to the original prompt, don't change it too much.\n"

    try:
        with llm_suggestion_lock:
            suggestion = get_llm_suggestions(
                prompt_value,
                improvement_instruction=instruction
            )
        return suggestion
    except Exception as e:
        return f"❌ Error: {str(e)}"

@callback(
    Output("keywords-suggestion-modal", "is_open"),
    Output("Prompt", "value", allow_duplicate=True),
    Input("accept-keywords-suggestion", "n_clicks"),
    Input("decline-keywords-suggestion", "n_clicks"),
    State("keywords-suggestion-modal-body", "children"),
    State("Prompt", "value"),
    prevent_initial_call=True
)
def handle_modal_action(accept_click, decline_click, suggestion_text, current_prompt):
    triggered = ctx.triggered_id
    if triggered == "accept-keywords-suggestion":
        return False, suggestion_text
    elif triggered == "decline-keywords-suggestion":
        return False, current_prompt
    raise PreventUpdate