from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
from helpers import sideBar
from pages import matrix_optimizer, data_selector
import dash_uploader as du
import os
import pandas as pd
import json

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
tmp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tmp')
du.configure_upload(app, tmp_path)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "color": "grey"
}

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sideBar.make_sidebar(),
    content
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    if pathname == "/":
        return data_selector.layout()
    if pathname == "/optimizer":
        return matrix_optimizer.layout()


def get_city_name(bfs_num):
    print(f'BFS_Nummer: {bfs_num}')
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'data')
    path = os.path.join(path, 'cities')
    filename = '00_bfs_numbers.json'
    path = os.path.join(path, filename)
    with open(path, 'r') as f:
        bfs_nummers = json.load(f)
    return bfs_nummers.get(str(bfs_num), f'{bfs_num} not found')

@du.callback(
    output=[Output('city-dropdown', 'options'), Output('parameter-dropdown', 'options'), Output('data-file-path', 'data')],
    id='upload-data',
)
def callback_on_completion(file_paths):
    if file_paths is not None:
        df = pd.read_csv(file_paths[0])
        # Save DataFrame to Parquet file
        
        # Update city dropdown options
        cities = df['bfs_nummer'].unique()
        city_options = [{'label': get_city_name(str(city)), 'value': str(city)} for city in cities]
        print('Successful options')

        # Update parameter dropdown options
        available_params = df.columns.difference(['d', 'year', 'geom', 'bfs_nummer']).tolist()
        parameter_options = [{'label': parameter, 'value': parameter} for parameter in available_params]

        return city_options, parameter_options, file_paths[0]
    else:
        return [], [], None
        
if __name__ == '__main__':
    from waitress import serve
    serve(server, host='0.0.0.0', port=8080, threads=100)
