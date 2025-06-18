from dash import callback, Output, Input, State, dash

from src.Dataset import Dataset
from src.widgets import scatterplot

@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    State('scatterplot', 'figure'),
    Input('scatterplot', 'relayoutData'),
    prevent_initial_call=True,
)
def zoomed_scatterplot(figure, zoom_data):
    if len(zoom_data) == 1 and 'dragmode' in zoom_data:
        return dash.no_update

    if 'xaxis.range[0]' not in zoom_data:
        return dash.no_update

    return scatterplot.add_images_to_scatterplot(figure)
