import os

import dash
import dash_cytoscape as cyto
import dash_html_components as html

import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from DataParser import kSpiderParser
from DataParser import JsonParser

ABS_PATH = os.path.dirname(os.path.realpath(__file__))

children_file_path = os.path.join(ABS_PATH, "sample_data/kSpider_children.tsv")
parents_file_path = os.path.join(ABS_PATH, "sample_data/parents.tsv")

Decoder = kSpiderParser(children_file= children_file_path , parents_file= parents_file_path)

JSON = JsonParser(os.path.join(ABS_PATH, "config.json"))

app = dash.Dash(__name__)

app.layout = html.Div([
    # The drop down menu HTML element for changing the layout. connected to a callback.
    dcc.Dropdown(
        id='dropdown-update-layout',
        value='grid',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
        ]
    ),
    cyto.Cytoscape(
        id=JSON.get_data("id"),
        layout=JSON.get_data("layout"),
        style=JSON.get_data("style"),
        elements=Decoder.get_elements(),
    )
])


# This call back for changing the layout dynamically by user selection
@app.callback(Output(JSON.get_data("id"), 'layout'), [Input('dropdown-update-layout', 'value')])
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


if __name__ == '__main__':
    app.run_server(debug=True)
