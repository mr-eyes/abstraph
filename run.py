import sys
import dash
import dash_cytoscape as cyto
import dash_html_components as html

from DataParser import kSpiderParser
from DataParser import JsonParser

JSON = JsonParser("config.json")
kSpider = kSpiderParser(sys.argv[1])


app = dash.Dash(__name__)


app.layout = html.Div([
    cyto.Cytoscape(
        id=JSON.get_data("id"),
        layout=JSON.get_data("layout"),
        style=JSON.get_data("style"),
        elements= kSpider.get_graph_elements(),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)