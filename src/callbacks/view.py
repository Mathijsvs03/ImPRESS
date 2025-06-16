from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc


@callback(
    Output("main-view", "children"),
    Input("view-toggle", "value"),
    Input("selected-image", "data"),
    prevent_initial_call=False
)

def update_main_view(view_mode, selected_image):
    if view_mode == "cluster":
        return dbc.Card([
            dbc.CardHeader("Clustered Dataset View"),
            dbc.CardBody(
                html.Div("This is where clustered images will appear.", style={
                    'height': '500px',
                    'backgroundColor': '#f1f3f5',
                    'border': '2px dashed #ccc',
                    'textAlign': 'center',
                    'lineHeight': '500px',
                    'color': '#666'
                })
            )
        ])
    else:
        return dbc.Card([
            dbc.CardHeader("Generated Image"),
            dbc.CardBody(
                dcc.Loading(
                    html.Img(src=selected_image, id="generated-image", style={
                        'maxWidth': '512px', 'maxHeight': '512px'
                    }),
                    type="circle"
                )
            )
        ])
