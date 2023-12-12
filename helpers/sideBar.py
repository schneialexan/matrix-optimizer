import dash_bootstrap_components as dbc
from dash import html


def make_sidebar():
    # styling the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
        "color": "grey",
        "overflow": "auto"
    }
    return html.Div(
        [
            html.Img(
                src="https://cdn.icon-icons.com/icons2/1223/PNG/512/1492617364-13-setting-configure-repair-support-optimization-google_83447.png",
                style={"width": "100%"}),
            html.Hr(),
            html.P("DAViS - Dashboard für EVA Matrix Optimierung"),
            dbc.Nav(
                [
                    dbc.NavLink("Daten Generierung", href="/", active="exact"),
                    dbc.NavLink("Matrix Optimierung", href="/optimizer", active="exact")
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )
