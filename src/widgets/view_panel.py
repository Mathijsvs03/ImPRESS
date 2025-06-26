from dash import dcc

from src.widgets.generated_panel import build_generated_panel
from src.widgets.cluster_panel import build_cluster_panel

def build_view_panel():
    return dcc.Tabs(
        id="view-toggle",
        value="generated",
        children=[
            dcc.Tab(build_generated_panel(), label="Selected Image", value="generated"),
            dcc.Tab(build_cluster_panel(), label="Clustered Images", value="cluster"),
        ]
    )
