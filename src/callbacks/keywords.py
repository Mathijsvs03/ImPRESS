from dash import Input, Output,callback, ALL

@callback(
    Output("generate-prompt-button-keywords", "style"),
    Input({"type": "keyword", "index": ALL}, "value"),
    prevent_initial_call=True
)
def set_prompt_from_keywords_visible(keywords):
    if keywords:
        return {"display": "inline-block"}
    else:
        return {"display": "none"}