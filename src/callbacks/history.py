from dash import html, callback, Output, Input, ALL, no_update, ctx
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
                html.H6(item["prompt"], className='mt-2 history-prompt')
            ], id={'type': 'thumb', 'index': i}, n_clicks=0,
                       className="hist-entry-button")
        ], className="history-entry")
        for i, item in enumerate(reversed(history))
    ]

@callback(
    Output("selected-image", "data"),
    Output("selected-prompt", "children"),
    Input({"type": "thumb", "index": ALL}, "n_clicks"),
    Input("history-store", "data"),
    prevent_initial_call=True
)
def history_clicked(n_clicks_list, history):
    triggered = ctx.triggered_id

    if triggered is None:
        return no_update
    elif triggered == "history-store":
        item = list(history)[-1]
    else:
        clicked_index = triggered["index"]

        history_reversed = list(reversed(history))

        item = history_reversed[clicked_index]

    return item["src"], item["prompt"]
