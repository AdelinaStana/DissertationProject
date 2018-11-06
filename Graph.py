class Graph:
    def __init__(self, database):
        self.db = database
        self.nodes = []
        self.edges = set()

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.append(name)

    def add_edge(self, x, y):
        if x < y:
            self.db.insert(x, y)
        else:
            self.db.insert(y, x)

    def number_of_edges(self):
        return self.db.count()

    def number_of_nodes(self):
        return len(self.nodes)

