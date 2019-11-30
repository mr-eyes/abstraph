import os
import json
import dash
import dash_cytoscape as cyto
import dash_html_components as html

import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from DataParser import DBRetinaParser
from DataParser import JsonParser

ABS_PATH = os.path.dirname(os.path.realpath(__file__))

namesMap_file_path = os.path.join(ABS_PATH, "sample_data/DBRetina/kProcessor_namesMap.tsv")
pairwise_file_path = os.path.join(ABS_PATH, "sample_data/DBRetina/kSpider_pairwise.tsv")
parents_file_path = os.path.join(ABS_PATH, "sample_data/DBRetina/parents_metadata.tsv")

Decoder = DBRetinaParser(namesMap_file_path, pairwise_file_path, parents_file_path)

# Load the configuration
JSON = JsonParser(os.path.join(ABS_PATH, "config.json"))

app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    }
]

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
    dcc.Checklist(
        options=[{'label': db_name, 'value': db_name} for db_name in Decoder.class_to_parents.keys()],
        # value=list(Decoder.class_to_parents.keys())
    ),
    cyto.Cytoscape(
        id=JSON.get_data("id"),
        layout=JSON.get_data("layout"),
        style=JSON.get_data("style"),
        stylesheet=default_stylesheet,
        elements=Decoder.get_elements(),
    ),
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre'])
])

##################
#   Callbacks
##################

# This call back for changing the layout dynamically by user selection
@app.callback(Output(JSON.get_data("id"), 'layout'), [Input('dropdown-update-layout', 'value')])
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


# This callback for printing the node information on Click
@app.callback(Output('cytoscape-tapNodeData-json', 'children'), [Input(JSON.get_data("id"), 'tapNodeData')])
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


###################
#   Main Function
###################

if __name__ == '__main__':
    app.run_server(debug=True)
