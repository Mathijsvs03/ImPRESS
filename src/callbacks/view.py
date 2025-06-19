from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from src.widgets.prompt_panel import build_prompt_panel
from src.widgets.keyword_panel import build_keyword_panel
from src.widgets import scatterplot


@callback(
    Output("main-view", "children"),
    Input("view-toggle", "value"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)

def update_main_view(view_mode, selected_image):
    if view_mode == "cluster":
        return dbc.Card([
            dbc.CardHeader("Clustered Dataset View"),
            dbc.CardBody(
                dcc.Loading(
                    scatterplot.create_scatterplot('UMAP'),
                    type="circle"
                )
            )
        ])
    else:
        return dbc.Card([
            dbc.CardHeader("Generated Image"),
            dbc.CardBody(
                dcc.Loading(
                    html.Img(src=selected_image, id="gen-image",
                             className="gen-image"),
                    type="circle"
                )
            )
        ])

@callback(
    Output("prompt-panel-container", "children"),
    Input("view-toggle", "value"),
    prevent_initial_call=False
)
def switch_prompt_panel(view_mode):
    keywords = ["Keyword 1", "Keyword 2", "Keyword 3"]
    if view_mode == "cluster":
        return build_keyword_panel(keywords)
    return build_prompt_panel(keywords)