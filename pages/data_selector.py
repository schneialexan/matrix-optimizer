from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import json
import os
import dash
import dash_uploader as du
import uuid
from helpers import helpers

def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['csv'],
        upload_id=uuid.uuid1(),  # Unique session id
    )

def layout():
    return html.Div([
        html.Div([
            html.H1("Data Selector for Matrix Optimization App"),
        ], style={'width': '100%', 'padding': '0px 20px 20px 20px', 'boxSizing': 'border-box', 'display': 'inline-block'}),
        
        get_upload_component('upload-data'),
        
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
    df = pd.read_csv(file_path)
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
    np.save(path + r'\\' + city_name + '.npy', matrices)
    
    # save parameters
    params_file_path = os.path.join(path, f'{city_name}_parameters.json')
    with open(params_file_path, 'w') as json_file:
        json.dump(selected_parameters, json_file)
    helpers.get_cities()
    return f'Saved {city_name}.npy and {city_name}_parameters.json'
