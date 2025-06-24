from dash import callback, Input, Output

@callback(
    Output("selected-prompt", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_selected_prompt(selected_image):
    """
    Keep the prompt‐text box in sync when you click on a thumbnail
    or after generating a new image.
    """
    if isinstance(selected_image, dict):
        return selected_image.get("prompt", "")
    return ""
