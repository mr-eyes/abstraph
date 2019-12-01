"""
Converting DBRetina files to a Cytoscape JSON file.

Input:
    - kProcessor resulted namesMap file.
    - kSpider Pairwise Similarity Matrix TSV.
    - Parents metadata TSV.

Output:
    - Compatible JSON file of elements with CytoScape.js.
"""

from DataParser import DBRetinaParser, JsonParser
import sys
import os
import json

namesMap_file_path = str()
pairwise_file_path = str()
parents_file_path = str()

if len(sys.argv) < 4:
    print("run: python dbretina_to_cytoscape.py <kSpider_pairwise> <namesMap> <parents_metadata>", file = sys.stderr)
    exit(1)
else:
    pairwise_file_path = sys.argv[1]
    namesMap_file_path = sys.argv[2]
    parents_file_path = sys.argv[3]

for file_path in [namesMap_file_path, pairwise_file_path, parents_file_path]:
    if not os.path.exists(file_path):
        print(f"error opening '{file_path}', file not found..", file=sys.stderr)
        sys.exit(1)

Decoder = DBRetinaParser(namesMap_file_path, pairwise_file_path, parents_file_path)
Decoder.export_elements()
