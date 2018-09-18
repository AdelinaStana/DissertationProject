from Config import Database


class Graph:
    def __init__(self):
        self.db = Database()
        self.db.connect_database()
        #db.create_table()
        self.nodes = []
        self.edges = set()

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.append(name)

    def add_edge(self, x, y):
        if (y, x) not in self.edges:
            self.edges.add((x, y))
        self.db.insert(x, y)

    def number_of_edges(self):
        self.db.execute()
        self.db.clear_table()
        return len(self.edges)

    def number_of_nodes(self):
        return len(self.nodes)

