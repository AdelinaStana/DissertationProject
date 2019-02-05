import csv
import pandas


class Graph:
    def __init__(self, name):
        self.csv_name = name
        self.file_writer = None
        self.create_file_writer_dict()
        self.nodes = set()

    def create_file_writer_dict(self):
        self.file_writer = open(self.csv_name+".csv", 'wt')
        self.file_writer.write("a,b\n")# header

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)

    def add_edge(self, x, y):
        if x < y:
            self.file_writer.write(str(x)+","+str(y)+"\n")
        else:
            self.file_writer.write(str(y)+","+str(x)+"\n")

    def number_of_edges(self):
        self.file_writer.close()
        data = pandas.read_csv(self.csv_name + ".csv")
        data = data.drop_duplicates(subset=['a', 'b'], keep='first')
        rows, columns = data.shape
        return rows

    def number_of_nodes(self):
        return len(self.nodes)

