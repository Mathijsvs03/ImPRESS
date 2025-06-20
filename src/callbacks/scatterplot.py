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


@callback(
    Output('scatterplot_selection', 'children'),
    Input('scatterplot', 'selectedData'),
    prevent_initial_call=True,
)
def on_selection_change(selected_data):
    if not selected_data or 'points' not in selected_data:
        return "No selection"

    selected_points = selected_data['points']
    selected_indices = [point['pointIndex'] for point in selected_points]

    dataset = Dataset.get_data()['train']
    selected_rows = dataset.select(selected_indices)
    return f"{len(selected_rows)} images selected"
