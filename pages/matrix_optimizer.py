import dash
from dash import html, dcc, dash_table, ctx
import numpy as np
from dash.dependencies import Input, Output, State
from optimizers import scipy_minimizer, sgd_minimizer, cvxpy_minimizer
from helpers import helpers
import os
import pandas as pd


def layout():
    START_MATRIX_SIZE = 4
    return html.Div([
        html.Div([
            html.H1("Matrix Optimization App"),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='stadt-dropdown',
                    options=[
                        {'label': city, 'value': city.lower()} for city in helpers.get_cities()
                    ],
                    value=helpers.get_cities()[0].lower(),
                ),
            ], style={'width': '60%', 'display': 'inline-block'}),
            html.Div([
                html.Div([
                    dcc.Markdown("Max Change:"),
                ], style={'display': 'inline-block'}),
                html.Div([
                    dcc.Input(  
                        id="max-change-input",
                        type="number",
                        placeholder="0.1",
                        value=0.1
                    ),
                ], style={'display': 'inline-block', 'marginLeft': '1em'}),
            ], style={'width': '30%', 'display': 'inline-block'}),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'flex', 'justifyContent': 'space-between'}),

        
        html.Div([
            dash_table.DataTable(
                id='matrix',
                style_cell={
                    'textAlign': 'center',          # numbers are in the middle
                    'minWidth': '50px',             # minimum size of column
                    'width': '50px', 
                    'maxWidth': '50px',
                    'overflow': 'hidden',           # text is clipped if too long
                    'textOverflow': 'ellipsis',     # text is clipped if too long
                },
                editable=True,
            ),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id="locked-indices",
                options=helpers.make_indices_from_matrixsize(START_MATRIX_SIZE),
                multi=True,
                placeholder="Select locked indices",
            ),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='optimization-method',
                options=[
                    {'label': 'Scipy Minimize', 'value': 'Scipy Minimize'},
                    {'label': 'SGD', 'value': 'SGD'},
                    {'label': 'CVXPY', 'value': 'CVXPY'},
                ],
                value='Scipy Minimize'
            ),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.Button("Optimize", id="optimize-button", style={'backgroundColor': '#6666FF', 'color': '#ffffff'}),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.Button("Reset", id="reset-button", style={'backgroundColor': '#ff0000', 'color': '#ffffff'}),
            ], style={'width': '50%', 'display': 'inline-block', 'textAlign': 'right'}),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        html.Div([
            html.Button("Save", id="save-button-matrix", style={'backgroundColor': '#00cc00', 'color': '#ffffff'}),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        html.Div(id='save-button-matrix-output'),
    ])


# New callback for saving the matrix
@dash.callback(
    Output('save-button-matrix-output', 'children'),
    [Input('save-button-matrix', 'n_clicks')],
    [State('matrix', 'data'),
     State('matrix', 'columns'),
     State('stadt-dropdown', 'value')]
)
def save_matrix(n_clicks, matrix_data, matrix_columns, stadt):
    if n_clicks is None:
        return dash.no_update
    df = pd.DataFrame(matrix_data)
    df.columns = [column['name'] for column in matrix_columns]
    save_folder = 'src/data/saved_matrices'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_path = os.path.join(save_folder, f'{stadt}_matrix_{n_clicks}.csv')
    df.to_csv(save_path, index=False)

    return f'Saved matrix as {save_path}'


def optimize_matrix(matrix, matrices, locked_indices, max_change, optimization_method):
    locked_indices = [] if locked_indices is None else [eval(index) for index in locked_indices]

    if optimization_method == 'Scipy Minimize':
        result, cost_list = scipy_minimizer.minimize_matrix(matrix, matrices, locked_indices, max_change)
    elif optimization_method == 'SGD':
        result = sgd_minimizer.minimize_matrix(matrix, matrices, locked_indices, max_change)
        result, cost_list = result
    elif optimization_method == 'CVXPY':
        result = cvxpy_minimizer.minimize_matrix(matrix, matrices, locked_indices, max_change)
    else:
        result = np.array(matrix)

    return helpers.make_dict_from_matrix(result)


# Main callback function
@dash.callback(
    [Output('matrix', 'data'), 
     Output('matrix', 'columns'), 
     Output('locked-indices', 'options')
     ],
    [Input('reset-button', 'n_clicks'), 
     Input('optimize-button', 'n_clicks'),
     Input('stadt-dropdown', 'value'),
     ],
    [State('max-change-input', 'value'),
     State("locked-indices", "value"), 
     State('matrix', 'data'), 
     State('optimization-method', 'value')
     ]
)
def update_matrix(reset_clicks, optimize_clicks, stadt, max_change, locked_indices, matrix, optimization_method):
    ctx_triggered = ctx.triggered_id

    # get necessary data
    matrices = np.load(f'src/data/cities/{stadt}.npy', allow_pickle=True)
    matrix_size = matrices[0].shape[1]

    print(f'Called with {ctx.triggered}')

    if 'reset-button' == ctx_triggered:
        return (
            helpers.make_initial_matrix(matrix_size),
            helpers.get_columns(stadt),
            helpers.make_indices_from_matrixsize(matrix_size)
        )

    if 'optimize-button' == ctx_triggered:
        matrix = helpers.make_matrix_from_dict(matrix)
        optimized_matrix = optimize_matrix(matrix, matrices, locked_indices, max_change, optimization_method)
        return (
            helpers.make_matrix(optimized_matrix, matrix_size),
            helpers.get_columns(stadt),
            helpers.make_indices_from_matrixsize(matrix_size)
        )
    
    return (
        helpers.make_initial_matrix(matrix_size),
        helpers.get_columns(stadt),
        helpers.make_indices_from_matrixsize(matrix_size)
    )