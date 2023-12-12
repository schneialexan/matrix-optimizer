from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import json
import base64
import io
import os
import tempfile
import dash

def layout():
    return html.Div([
        html.Div([
            html.H1("Data Selector for Matrix Optimization App"),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop a .csv or ',
                html.A('Select a .csv File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        
        dcc.Loading(
            id='loading-output',
            type='circle',  # You can customize the loading spinner type
            children=[
                html.Div([
                    dcc.Store(id='data-file-path', storage_type='local'),  # Store to save the data
                    
                    html.Div([
                        html.Label('Select City:'),
                        dcc.Dropdown(
                            id='city-dropdown',
                            value=None
                        ),
                    ], style={'width': '50%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label('Select Parameters:'),
                        dcc.Dropdown(
                            id='parameter-dropdown',
                            multi=True,
                        ),
                    ], style={'width': '50%', 'display': 'inline-block'}),

                    html.Button('Save as .npy', id='save-button-selector'),
                    html.Div(id='save-button-output'),
                ]),
            ],
        ),
    ])


def get_city_name(bfs_num):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, 'data')
    path = os.path.join(path, 'cities')
    filename = '00_bfs_numbers.json'
    path = os.path.join(path, filename)
    with open(path, 'r') as f:
        bfs_nummers = json.load(f)
    return bfs_nummers.get(str(bfs_num), f'{bfs_num} not found')

# Callback to update data file and dropdowns
@dash.callback(
    [Output('city-dropdown', 'options'),
     Output('parameter-dropdown', 'options'),
     Output('data-file-path', 'data')],
    [Input('upload-data', 'contents')],
    prevent_initial_call=True
)
def update_data_and_dropdowns(contents):
    content_type, content_string = contents.split(',')
    decoded = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    df = pd.read_csv(decoded)
    
    # Save DataFrame to Parquet file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, 'data.parquet')
    df.to_parquet(file_path, index=False)

    # Update city dropdown options
    cities = df['bfs_nummer'].unique()
    city_options = [{'label': get_city_name(str(city)), 'value': str(city)} for city in cities]

    # Update parameter dropdown options
    available_params = df.columns.difference(['d', 'year', 'geom', 'bfs_nummer']).tolist()
    parameter_options = [{'label': parameter, 'value': parameter} for parameter in available_params]

    return city_options, parameter_options, file_path

# Callback to save selected parameters as .npy file
@dash.callback(
    Output('save-button-output', 'children'),
    [Input('save-button-selector', 'n_clicks')],
    [State('city-dropdown', 'value'),
     State('parameter-dropdown', 'value'),
     State('data-file-path', 'data')],
    prevent_initial_call=True
)
def save_parameters(n_clicks, city_value, selected_parameters, file_path):
    df = pd.read_parquet(file_path)
    city_data = df[df['bfs_nummer'] == int(city_value)]
    matrices = []

    for year in city_data.year.unique().tolist():
        data = city_data[city_data['year'] == year][selected_parameters]
        matrices.append(data.to_numpy())
    
    city_name = get_city_name(city_value).lower()

    # save matrices
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, 'data')
    path = os.path.join(path, 'cities')
    np.save(path + city_name + '.npy', matrices)
    
    # save parameters
    params_file_path = os.path.join(path, f'{city_name}_parameters.json')
    with open(params_file_path, 'w') as json_file:
        json.dump(selected_parameters, json_file)

    return f'Saved {city_name}.npy and {city_name}_parameters.json'
