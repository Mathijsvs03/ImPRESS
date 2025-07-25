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
import src.callbacks.keywords
import src.callbacks.llm_suggestion
import src.callbacks.scatterplot
import src.callbacks.prompt_panel
import src.callbacks.generator_state
import src.callbacks.keyword_state
import src.callbacks.img_download

os.environ['FLASK_ENV'] = 'development'


def run_ui(initial_history=None):
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ]
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
        dcc.Store(id="is-generating",    data=False),
        # html.H1('ImPress', className='header-title'),

        dbc.Row([
            dbc.Col(input_panel_widget, className="main-col", width=4, style={"height": "100%", "padding-bottom": "10px"}),
            dbc.Col(view_panel_widget, className="main-col with-divider", width=8, style={"height": "100%", "padding-bottom": "10px"})
        ], className='top-row', style={"height": "80%"}),
        dbc.Row([
            dbc.Col(build_history_panel(), className="main-col", style={"height": "100%"})
        ], className='bottom-row', style={"height": "20%"})
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
