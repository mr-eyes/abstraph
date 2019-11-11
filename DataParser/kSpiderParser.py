class kSpiderParser:

    __pairwise_matrix = list()
    __graph_elements = list()

    nodes = list()
    edges = list()

    def __init__(self, filename):
        with open(filename, 'r') as sample:
            next(sample) #skip the header
            for line in sample:
                line = line.strip().split('\t')
                seq_1 = line[0]
                seq_2 = line[1]
                shared = line[3]
                
                self.nodes.append({'data': {'id': seq_1, 'label': "seq" + seq_1},})
                self.nodes.append({'data': {'id': seq_2, 'label': "seq" + seq_2},})
                self.edges.append({'data': {'source': seq_1, 'target': seq_2}, 'style' : {'width' : int(float(shared) % 5)}})

        
        self.__graph_elements = self.nodes + self.edges


    def get_pairwise(self):
        return self.__pairwise_matrix

    def get_graph_elements(self):
        return self.__graph_elements