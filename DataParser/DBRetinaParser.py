import random

"""
Description:
    - Parse the DBRetina output and export it in a json file.

Input: 
    - kProcessor resulted namesMap file.
    - kSpider Pairwise Similarity Matrix TSV.
    - Parents metadata TSV.

Output:
    - Compatible JSON file of elements with CytoScape.js.
"""


class DBRetinaParser:
    children_file = str()
    parents_file = str()
    kProcessor_namesMap_file = str()

    nodes = list()
    edges = list()
    elements = list()

    parents_set = set()

    parent_to_children = dict()
    child_to_parents = dict()
    parent_to_class = dict()
    class_to_parents = dict()
    class_to_color = dict()
    namesMap = dict()

    def __init__(self, kProcessor_namesMap, pairwise_tsv, parents_file):
        self.kProcessor_namesMap_file = kProcessor_namesMap
        self.children_file = pairwise_tsv
        self.parents_file = parents_file

        self.parse_namesMap()
        self.parse_parents()
        self.classes_coloring()
        self.construct_nodes()
        self.construct_edges()

    def parse_namesMap(self):
        with open(self.kProcessor_namesMap_file, 'r') as namesMap_reader:
            next(namesMap_reader)  # Skip the total names count line
            for line in namesMap_reader:
                line = line.strip().split(" ")
                self.namesMap[line[0]] = line[1]

    def construct_edges(self):
        """
        Parsing children TSV file generated from kSpider.

        TSV structure:
            parent1    parent2    shared_children
        
        This should be handled as graph weighted edges.
        """

        with open(self.children_file, 'r') as children_reader:
            next(children_reader)  # skip the header

            for child_line in children_reader:
                line = child_line.strip().split()
                parent1_id = line[0]
                parent2_id = line[1]
                shared_children_no = line[2]

                self.elements.append(
                    {
                        'data': {'source': parent1_id, 'target': parent2_id},
                        'style': {'label': shared_children_no},
                    }
                )

    def parse_parents(self):
        """
        Parsing the parents file.

        TSV structure:
            parent  database

        """

        with open(self.parents_file, 'r') as parents_reader:
            next(parents_reader)  # skip the first line
            for parent_line in parents_reader:
                line = parent_line.strip().split()
                parent_id = line[0]
                parent_class = line[1]
                self.parent_to_class[parent_id] = parent_class

                # Fill dict: parent_to_children
                if parent_class in self.class_to_parents:
                    self.class_to_parents[parent_class].append(parent_id)
                else:
                    self.class_to_parents[parent_class] = [parent_id]

    def classes_coloring(self):
        classes_names = list(self.class_to_parents.keys())
        number_of_classes = len(classes_names)

        all_colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                      for i in range(number_of_classes)]

        for idx, class_name in enumerate(classes_names):
            self.class_to_color[class_name] = all_colors[idx]

    def construct_nodes(self):

        for parent_id, parent_class in self.parent_to_class.items():
            # print(f"parent_id: {parent_id}, parent_class: {parent_class}")
            self.elements.append(
                {
                    'data': {'id': parent_id, 'label': parent_id},
                    'style': {"background-color": self.class_to_color[parent_class]}
                }
            )

    def get_elements(self):
        return self.elements
