from PIL import Image
from dash import dcc
import plotly.express as px
from src.Dataset import Dataset
from src import config
import plotly.graph_objects as go


def add_images_to_scatterplot(figure):
    figure['layout']['images'] = []
    scatterplot_data = figure['data'][0]
    scatter_images = scatterplot_data['customdata']
    scatter_x = scatterplot_data['x']
    scatter_y = scatterplot_data['y']

    min_x, max_x = figure['layout']['xaxis']['range']
    min_y, max_y = figure['layout']['yaxis']['range']

    images_in_zoom =[]
    for x, y, image in zip(scatter_x, scatter_y, scatter_images):
        if min_x <= x <= max_x and min_y <= y <= max_y:
            images_in_zoom.append((x, y, image))
        if len (images_in_zoom) > config.MAX_IMAGES_IN_ZOOM:
            return figure

    if images_in_zoom:
        print(images_in_zoom[0])
        for x, y, image in images_in_zoom:
            figure['layout']['images'].append(dict(
                x=x,
                y=y,
                source=Image.open(image),
                xref='x',
                yref='y',
                sizex=0.05,
                sizey=0.05,
                xanchor='center',
                yanchor='middle',
            ))
        return figure
    return figure


def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'tsne_x', 'tsne_y'
    elif projection == 'UMAP':
        x_col, y_col = 'umap_x', 'umap_y'
    else:
        raise ValueError(f"Unknown projection type: {projection}")

    fig = px.scatter(
        Dataset.get_data()['train'],
        x=x_col,
        y=y_col,
    )

    fig.update_traces(
        customdata=Dataset.get_data()['train']['image'],
        marker={'color': 'rgba(31, 119, 180, 0.5)', 'size': 4},
        unselected_marker_opacity=0.60
    )
    fig.update_layout(dragmode='select')
    fig.update_xaxes(titlefont=dict(size=12), tickfont=dict(size=10))
    fig.update_yaxes(titlefont=dict(size=12), tickfont=dict(size=10), scaleanchor="x", scaleratio=1)
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            name='image embedding',
            marker=dict(size=7, color='blue', symbol='circle'),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            name='selected class',
            marker=dict(size=7, color="red", symbol='circle'),
        ),
    )
    fig.update_traces(
        hoverinfo='skip', hovertemplate=None,
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))

    return fig


def create_scatterplot(projection):
    return dcc.Graph(
        figure=create_scatterplot_figure(projection),
        id='scatterplot',
        responsive=True,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['autoscale']
        },
        className="cluster-field"
    )


def get_selected_data(figure):
    figure_data = figure['data'][0]
    dataset = Dataset.get_data()['train']
    if 'selectedpoints' in figure_data:
        selected_images = list(map(figure_data['customdata'].__getitem__, figure_data['selectedpoints']))
        data_selected = dataset.loc[selected_images]
    else:
        data_selected = dataset

    return data_selected