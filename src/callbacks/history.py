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
                html.Img(src=item["src"], className="history-image"),
                html.H6(item["prompt"], className='mt-2')
            ], id={'type': 'thumb', 'index': i}, n_clicks=0,
                       className="hist-entry-button")
        ], className="history-entry")
        for i, item in enumerate(reversed(history))
    ]
