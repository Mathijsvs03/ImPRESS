from dash import html, dcc, callback, Output, Input


@callback(
    Output("gen-image-container", "children"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)
def update_image_display(selected_image):
    if selected_image:
        return html.Img(src=selected_image["src"], className="gen-image")
    return html.Div("No image selected", className="image-field")