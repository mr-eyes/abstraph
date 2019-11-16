import dash
import dash_cytoscape as cyto
import dash_html_components as html

import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from DataParser import listDecoderParser
from DataParser import JsonParser

Decoder = listDecoderParser(children_file="sample_data/children.tsv", parents_file="sample_data/parents.tsv")

app = dash.Dash(__name__)

JSON = JsonParser("config.json")

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
