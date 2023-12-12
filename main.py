from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
from helpers import sideBar
from pages import matrix_optimizer, data_selector

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

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
        
server = app.server
if __name__ == '__main__':
    app.run()
