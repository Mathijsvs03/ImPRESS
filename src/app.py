from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os

from src.Dataset import Dataset
from src.llm_utils import get_llm_model
from src.utils import get_projector_models
from src.widgets.input_panel import build_input_panel
from src.widgets.view_panel import build_view_panel
from src.widgets.history_panel import build_history_panel

import src.callbacks.view
import src.callbacks.generator
import src.callbacks.history
import src.callbacks.llm_suggestion
import src.callbacks.scatterplot
import src.callbacks.prompt_panel

os.environ['FLASK_ENV'] = 'development'  # Auto-update style.css changes


def run_ui(initial_history=None):
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True
    )

    input_panel_widget = build_input_panel()
    view_panel_widget = build_view_panel()

    app.layout = dbc.Container([
        dcc.Store(id='stored-selection', data=None),
        dcc.Store(id="history-store", data=initial_history or []),
        dcc.Store(id="selected-image", data=(initial_history[0] if initial_history else "")),
        html.H1('ImPress', className='header-title'),

        dbc.Row([
            # Left column
            dbc.Col(
                input_panel_widget,
                className="h-100 d-flex flex-column left-col",
                width=4
            ),

            # Right column
            dbc.Col([
                view_panel_widget,
                build_history_panel()],
                width=8
            )
        ], className='gx-4 gy-2 col-container', align='start')
    ], className='main-container', fluid=True)

    app.run(debug=True, use_reloader=False, port=8050)


def main():
    Dataset.load()
    get_llm_model()
    get_projector_models()

    print("Starting Dash App")
    run_ui(initial_history=[])


if __name__ == '__main__':
    main()
