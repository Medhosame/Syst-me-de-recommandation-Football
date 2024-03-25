import dash
from dash import Dash, html, dcc,Output,Input
import pandas as pd


app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container,
    dcc.Store(id="store"),
])
if __name__ == '__main__':
    app.run(debug=True)