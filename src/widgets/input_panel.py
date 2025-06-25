import dash_bootstrap_components as dbc
from dash import html, dcc

from src.widgets.prompt_panel import build_prompt_panel
from src.widgets.keyword_panel import build_keyword_panel

def build_input_panel():
    return dcc.Tabs(
        id="input-toggle",
        value="prompt",
        children=[
            dcc.Tab(build_prompt_panel(), label="Prompt", value="prompt"),
            dcc.Tab(build_keyword_panel(), label="Keywords", value="keyword"),
        ]
    )

