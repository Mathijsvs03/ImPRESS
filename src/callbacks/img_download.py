from dash import Input, Output, State, callback, dash, dcc
import uuid
import base64

@callback(
    Output("download-image", "data"),
    Input("download-image-button", "n_clicks"),
    State("selected-image", "data"),
    prevent_initial_call=True
)
def trigger_download(n_click, selected):
    if not selected or "src" not in selected:
        return dash.no_update

    base64_data = selected["src"].split(",")[1]  # Extract base64 part
    decoded = base64.b64decode(base64_data)
    return dcc.send_bytes(decoded, filename=f"gen_img_{uuid.uuid4().hex}.png")