from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import base64
import os

from src.Dataset import Dataset
from src.widgets.prompt_panel import build_prompt_modal
from src.widgets.view_panel import build_view_panel
from src.widgets.history_panel import build_history_panel

import src.callbacks.generator
import src.callbacks.history
import src.callbacks.view
import src.callbacks.llm_suggestion

os.environ['FLASK_ENV'] = 'development' # Auto-update style.css changes

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
    modal_container = html.Div(build_prompt_modal(), className='modal-container')

    app.layout = dbc.Container([
        dcc.Store(id="history-store", data=initial_history),
        dcc.Store(id="selected-image", data=initial_history[0]["src"] if initial_history else ""),
        html.H1('ImPress', className='header-title'),

        dbc.Row([
            # Left column in app view
            dbc.Col(
                html.Div([
                    prompt_panel_container,
                    modal_container
                ]),
                className="h-100 d-flex flex-column left-col",
                width=4
            ),

            # Right column in app view
            dbc.Col(
                dbc.Stack([
                    view_panel_widget,
                    html.Hr(),
                    history_panel_widget
                ]),
                width=8
            )
        ], className='gx-4 gy-2 col-container', align='start')
    ], className='main-container', fluid=True)

    app.run(debug=True, use_reloader=False)


def main():
    Dataset.load()

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

    print("Starting Dash App")
    run_ui(initial_history=template_history)


if __name__ == '__main__':
    main()
