class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = set()

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.append(name)

    def add_edge(self, x, y):
        if not ((x, y) in self.edges) and not ((y, x) in self.edges):
            self.edges.add((x, y))

    def number_of_edges(self):
        return len(self.edges)

    def number_of_nodes(self):
        return len(self.nodes)

