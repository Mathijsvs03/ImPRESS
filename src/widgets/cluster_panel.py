import dash_bootstrap_components as dbc

from src.widgets.scatterplot import create_scatterplot

def build_cluster_panel():
    return create_scatterplot('UMAP')