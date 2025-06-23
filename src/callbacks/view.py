from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from src.widgets.prompt_panel import build_prompt_panel
from src.widgets.keyword_panel import build_keyword_panel
from src.widgets.history_panel import build_history_panel

@callback(
    Output("gen-image", "src"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)

def update_main_view(selected_image):
    return selected_image