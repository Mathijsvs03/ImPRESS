from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_split_pane

# df = pd.read_csv('data.csv')

app = Dash()

# plotly_figure = px.line(df[df['country']=='Canada'], x='year', y='pop')

# Temp keywords distribution features
keywords = ['Keyword 1', 'Keyword 2', 'Keyword 3']

keyword_dists = [
    html.Div([
        html.H4(kw),
        html.Div("Distribution graph", style={'height': '100px', 'background': '#829198'})
        ], style={'padding': '10px',
            'borderBottom': '1px solid #ccc'})
    for kw in keywords
]

key_dist_list = html.Div(
    keyword_dists,
    style={
        'height': '100%',
        'overflowY': 'scroll',
        'padding': '10px'
    }
)


# History list
history = ["Prompt 1", "Prompt 2", "Prompt 3", "Prompt 4", "Prompt 5", "Prompt 6", "Prompt 7"]

history_entries = [
    html.Div([
        html.Div("Generated image", style={'height': '150px', 'background': '#829198'}),
        html.H4(hs)
        ], style={
                'minWidth': '200px',
                'marginRight': '10px',
                'padding': '10px',
                'border': '1px solid #ccc',
                'borderRadius': '5px',
                'boxSizing': 'border-box',
                'backgroundColor': '#f5f5f5'
            })
    for hs in history
]

hist_list = html.Div(
    history_entries,
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'overflowX': 'auto',
        'padding': '10px',
        'height': '100%',
        'whiteSpace': 'nowrap',
        'border': '1px solid #aaa'
    }
)


app.layout = html.Div([
    # App title header
    html.H1('New visual analysis system name', style={'textAlign':'left', 'margin': '10px'}),

    # Main horizontal split containers
    dash_split_pane.DashSplitPane(
        split="vertical",
        # minSize=200,
        # maxSize=1000,
        size="23%",
        style={'borderTop': '2px solid #000', 'width': '100%'},
        children=[

            # Vertical split in left column
            dash_split_pane.DashSplitPane(
                split="horizontal",
                # minSize=300,
                # maxSize=1000,
                size="31%",
                style={'width': '100%'},
                children=[
                    # Prompt corner
                    html.Div([
                        html.Textarea(id="Prompt", placeholder="Enter your image generation prompt",
                            style={'height': '30%', 'width': '100%'}),
                        html.Textarea(id="NegPrompt", placeholder="Enter your negative prompt (optional)",
                            style={'height': '15%', 'width': '100%'}),
                        html.Div("Guidance Scale", style={"marginTop": '10px'}),
                        dcc.RangeSlider(0, 50, 1, value=[5, 15], allowCross=False,
                            marks={0: '0', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50'},
                            tooltip={"placement": "bottom", "always_visible": True}),
                        html.Button("Generate image",
                            style={'marginTop': '10px', 'fontSize': '24px', 'display': 'inline-block'})
                    ], style={'width': '100%', 'padding': '3px', 'paddingRight': '12px'}),
                    # Keyword distribution corner
                    html.Div([
                        html.Button("Generate prompt",
                            style={'marginTop': '10px', 'fontSize': '24px', 'display': 'inline-block'}),
                        key_dist_list
                    ])
                ]
            ),

            # Vertical split in right column
            dash_split_pane.DashSplitPane(
                split="horizontal",
                # minSize=300,
                # maxSize=1000,
                size="70%",
                children=[
                    # Clustered images corner
                    html.Div("Clustered dataset images", style={
                        'height': '100%', 'width': '100%', 'padding': '20px'
                    }),
                    # History corner
                    hist_list
                ]
            )
        ]
    )
], style={'height': '100vh'}
)

# @callback(
#     Output('graph-content', 'figure'),
#     Output('bar-plot', 'figure'),
#     Input('dropdown-selection', 'value'),
# )
# def update_graph(value):
#     dff = df[df['country']==value]
#     return (px.line(dff, x='year', y='pop'), px.bar(dff, x='year', y='pop')
# )

# @callback(
#     Output('dropdown-selection', 'value'),
#     Input('submit-val', 'n_clicks'),
#     prevent_initial_call=True
# )
# def update_clicks(n_clicks):
#     countries = df['country'].unique()
#     return countries[n_clicks % len(countries)]

app.run(debug=True)


