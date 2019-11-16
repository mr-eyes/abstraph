import random


class listDecoderParser:
    children_file = str()
    parents_file = str()

    nodes = list()
    edges = list()
    elements = list()

    parent_to_children = dict()
    child_to_parents = dict()
    parent_to_class = dict()
    class_to_parents = dict()
    class_to_color = dict()

    def __init__(self, children_file, parents_file):
        self.children_file = children_file
        self.parents_file = parents_file

        self.parse_children()
        self.parse_parents()
        self.classes_coloring()
        self.construct_nodes()
        self.construct_edges()

    def parse_children(self):
        with open(self.children_file, 'r') as children_reader:
            next(children_reader)  # skip the header

            for child_line in children_reader:
                line = child_line.strip().split()
                parent_id = line[0]
                child_id = line[1]

                # Fill dict: parent_to_children
                if parent_id in self.parent_to_children:
                    self.parent_to_children[parent_id].append(child_id)
                else:
                    self.parent_to_children[parent_id] = [child_id]

                # Fill dict: child_to_parents
                if child_id in self.child_to_parents:
                    self.child_to_parents[child_id].append(parent_id)
                else:
                    self.child_to_parents[child_id] = [parent_id]

    def parse_parents(self):
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
            self.nodes.append(
                {
                    'data': {'id': parent_id, 'label': parent_id},
                    'style': {"background-color": self.class_to_color[parent_class]}
                }
            )

    def construct_edges(self):
        for parent_id_1, parent_children_1 in self.parent_to_children.items():
            parent_children_1 = set(parent_children_1)
            for parent_id_2, parent_children_2 in self.parent_to_children.items():
                if parent_id_1 == parent_id_2:
                    continue

                parent_children_2 = set(parent_children_2)

                children_intersection = parent_children_1.intersection(parent_children_2)
                number_of_shared_children = len(children_intersection)

                # Don't create an edge if there are no shared children
                if number_of_shared_children == 0:
                    continue

                self.edges.append(
                    {
                        'data': {'source': parent_id_1, 'target': parent_id_2},
                        'style': {'label': str(number_of_shared_children)},
                    }
                )

                # Add nodes to edges to create the Cytoscape's elements
                self.elements = self.nodes + self.edges

    def get_elements(self):
        return self.elements
