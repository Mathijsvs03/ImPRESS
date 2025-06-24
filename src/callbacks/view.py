from dash import callback, Input, Output, html

@callback(
    Output("selected-prompt", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_selected_prompt(selected_image):
    """
    Show the actual prompt when an image is selected,
    otherwise show a friendly placeholder.
    """
    placeholder = "Your prompt will appear here once you generate an image."
    if isinstance(selected_image, dict):
        return selected_image.get("prompt", placeholder)
    return placeholder
