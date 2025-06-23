from dash import callback, Output, Input

@callback(
    Output("gen-image", "src"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_main_view(selected_image):
    return selected_image

@callback(
    Output("selected-prompt", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_prompt(selected_image):
    return selected_image["prompt"]