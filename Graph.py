import csv
import pandas


class Graph:
    def __init__(self, name):
        self.csv_name = name
        self.csv_file = open(self.csv_name, 'wt')
        self.file_writer = csv.writer(self.csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.file_writer.writerow(['a', 'b'])
        self.nodes = set()

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)

    def add_edge(self, x, y):
        if x < y:
            self.file_writer.writerow([x, y])
        else:
            self.file_writer.writerow([y, x])

    def number_of_edges(self):
        self.csv_file.close()
        data = pandas.read_csv(self.csv_name)
        data = data.drop_duplicates(subset=['a', 'b'], keep='first')
        rows, columns = data.shape
        return rows

    def number_of_nodes(self):
        return len(self.nodes)

