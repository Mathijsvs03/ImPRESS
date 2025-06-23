from dash import callback, Output, Input, html


@callback(
    Output("gen-image", "src"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_main_view(selected_image):
    if not selected_image or isinstance(selected_image, str) and selected_image == "":
        return "" 
    return selected_image["src"] if isinstance(selected_image, dict) else selected_image

@callback(
    Output("selected-prompt", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_prompt(selected_image):
    if isinstance(selected_image, dict):
        return selected_image.get("prompt", "")
    return ""

    from dash import Output, Input, callback, html

@callback(
    Output("generated-content", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_generated_content(selected_image):
    if not selected_image:
        return html.P(
            "Please generate an image to begin inspecting it.",
            className="placeholder-text"
        )

    src = selected_image.get("src") if isinstance(selected_image, dict) else selected_image
    return html.Img(src=src, className="gen-image", alt="Generated image")
