from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc


@callback(
    Output("image-history", "children"),
    Input("history-store", "data")
)
def update_history_display(history):
    return [
        dbc.Card([
            dbc.Button([
                html.Img(src=item["src"], style={'height': '150px', 'width': '100%', 'objectFit': 'cover'}),
                html.H6(item["prompt"], className='mt-2')
            ], id={'type': 'thumb', 'index': i}, n_clicks=0, style={
                'border': 'none',
                'background': 'none',
                'textAlign': 'left',
                'width': '100%'
            })
        ], style={
            'minWidth': '200px',
            'marginRight': '10px',
            'padding': '10px',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'backgroundColor': '#f8f9fa'
        })
        for i, item in enumerate(reversed(history))
    ]
