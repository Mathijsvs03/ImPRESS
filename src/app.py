from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import base64
import os

from src.Dataset import Dataset
from src.llm_utils import get_llm_model
from src.utils import get_projector_models
from src.widgets.history_panel import build_history_panel
from src.widgets.keyword_panel import build_keyword_panel
from src.widgets.prompt_panel import build_prompt_panel
from src.widgets.scatterplot import create_scatterplot
from src.widgets.image_display import create_image_display

import src.callbacks.generator
import src.callbacks.history
import src.callbacks.llm_suggestion
import src.callbacks.scatterplot
import src.callbacks.image_display

os.environ['FLASK_ENV'] = 'development' # Auto-update style.css changes

def run_ui(initial_history=None):
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True
    )

    left_tab = dcc.Tabs([
        dcc.Tab(label="Prompt", value="prompt", children=build_prompt_panel()),
        dcc.Tab(label="Keywords", value="keyword", children=build_keyword_panel()),
    ], id="input-togle", value="prompt")

    right_tab = dcc.Tabs([
        dcc.Tab(label="Generated Image", value="generated", children=create_image_display()),
        dcc.Tab(label="Clustered View", value="cluster", children=create_scatterplot('UMAP'))
    ], id="view-toggle", value="generated")

    app.layout = dbc.Container([
        dcc.Store(id="history-store", data=initial_history),
        dcc.Store(id="selected-image", data=initial_history[0] if initial_history else ""),
        html.H1('ImPress', className='header-title'),

        dbc.Row([
            # Left column in app view
            dbc.Col(
                left_tab,
                className="h-100 d-flex flex-column left-col",
                width=4
            ),

            # Right column in app view
            dbc.Col(
                dbc.Stack([
                    right_tab,
                    html.Hr(),
                    build_history_panel()
                ]),
                width=8
            )
        ], className='gx-4 gy-2 col-container', align='start')
    ], className='main-container', fluid=True)

    app.run(debug=True, use_reloader=False, port=8059)


def main():
    Dataset.load()
    get_llm_model()
    get_projector_models()

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
