from dash import callback, Output, Input, State, dash
from collections import Counter
from keybert import KeyBERT

from src.Dataset import Dataset
from src.widgets import scatterplot
from src.widgets.keyword_panel import build_keyword_content
from src.llm_utils import filter_style_keywords

kw_model = KeyBERT(model='all-MiniLM-L6-v2')

@callback(
    Output("scatterplot", "figure"),
    Input("view-toggle", "value"),
    State("scatterplot", "figure"),
    prevent_initial_call=True
)
def reset_scatterplot(view, figure):
    if view == 'cluster':
        return dash.no_update

    figure["layout"]["xaxis"]["autorange"] = True
    figure["layout"]["yaxis"]["autorange"] = True
    return figure


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
    Output('keyword-content', 'children'),
    Input('scatterplot', 'selectedData'),
    prevent_initial_call=True,
)
def on_selection_change(selected_data):
    if not selected_data or "points" not in selected_data or len(selected_data["points"]) == 0:
        return dash.no_update

    selected_points = selected_data['points']

    prompts = []
    for point in selected_points:
            prompts.append(point['text'])

    all_keywords = []
    for prompt in prompts:
        keywords = kw_model.extract_keywords(
            prompt,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            use_maxsum=True,
            nr_candidates=20,
            top_n=5
        )
        all_keywords.extend([kw[0] for kw in keywords])

    keyword_counts = Counter(all_keywords)
    candidate_keywords = [kw for kw, _ in keyword_counts.most_common(10)]
    style_keywords = filter_style_keywords(candidate_keywords, top_n=3)

    return build_keyword_content(style_keywords)

@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    Input('selected-image', 'data'),
    State('scatterplot', 'figure'),
    prevent_initial_call=True,
)
def highlight_selected_image(selected_image, figure):
    if not selected_image:
        figure['data'][0]['marker']['color'] = 'rgba(31, 119, 180, 0.5)'
        return figure

    projection_coords = selected_image.get('projection_coords', None)
    if not projection_coords:
        figure['data'][0]['marker']['color'] = 'rgba(31, 119, 180, 0.5)'
        return figure

    sel_x, sel_y = projection_coords['umap_x'], projection_coords['umap_y']
    x_vals, y_vals = figure['data'][0]['x'], figure['data'][0]['y']

    colors = [
        'red' if abs(x - sel_x) < 1e-6 and abs(y - sel_y) < 1e-6
        else 'rgba(31, 119, 180, 0.5)'
        for x, y in zip(x_vals, y_vals)
    ]

    figure['data'][0]['marker']['color'] = colors
    return figure