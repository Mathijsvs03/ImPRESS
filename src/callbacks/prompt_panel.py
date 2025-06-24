from dash import Input, Output, callback

@callback(
    Output("prompt-tools-container", "style"),
    Input("Prompt", "value")
)
def toggle_prompt_tools(prompt_text):
    if prompt_text and len(prompt_text.strip()) > 0:
        return {"display": "block"}
    return {"display": "none"}