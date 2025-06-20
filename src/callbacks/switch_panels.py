from dash import callback, Output, Input, dash
from src.widgets.keyword_panel import build_keyword_panel
from src.widgets.prompt_panel import build_prompt_panel
from src.widgets.scatterplot import create_scatterplot_figure

@callback(
    Output("prompt-panel-container", "children"),
    Output("scatterplot", "figure"),
    Input("view-toggle", "value"),
    prevent_initial_call=False
)
def switch_prompt_panel(view_mode):
    keywords = ["Keyword 1", "Keyword 2", "Keyword 3"]
    if view_mode == "cluster":
        return build_keyword_panel(keywords), dash.no_update
    return build_prompt_panel(keywords), create_scatterplot_figure('UMAP')