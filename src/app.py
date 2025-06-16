from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import base64
import os

from widgets.prompt_panel import build_prompt_modal
from widgets.view_panel import build_view_panel
from widgets.history_panel import build_history_panel

import callbacks.generator
import callbacks.history
import callbacks.view
import callbacks.llm_suggestion


def run_ui(initial_history=None):
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True
    )

    prompt_panel_container = html.Div(id="prompt-panel-container")
    view_panel_widget = build_view_panel()
    history_panel_widget = build_history_panel()
    modal_container = html.Div(build_prompt_modal(), style={"display": "none"})

    app.layout = dbc.Container([
        dcc.Store(id="history-store", data=initial_history),
        dcc.Store(id="selected-image", data=initial_history[0]["src"] if initial_history else ""),
        html.H1('ImPress', style={'textAlign': 'left', 'margin': '10px'}),

        dbc.Row([
            dbc.Col(
                html.Div([
                    prompt_panel_container,
                    modal_container
                ]),
                style={'borderRight': '1px solid #ccc', 'paddingRight': '15px'},
                className="h-100 d-flex flex-column",
                width=4
            ),

            dbc.Col(
                dbc.Stack([
                    view_panel_widget,
                    html.Hr(),
                    history_panel_widget
                ]),
                width=8
            )
        ], className='gx-4 gy-2', align='start', style={'height': '100%', 'overflowY': 'auto'})
    ], fluid=True, style={"height": "100%"})

    app.run(debug=True, use_reloader=False)


def main():
    folder = "src/assets/templates"
    template_history = []
    if not os.path.exists(folder):
        template_history = []

    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder, filename)
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                src = f"data:image/png;base64,{encoded}"
                template_history.append({"src": src, "prompt": f"Template: {filename}"})

    print("Starting Dash app")
    run_ui(initial_history=template_history)


if __name__ == '__main__':
    main()
