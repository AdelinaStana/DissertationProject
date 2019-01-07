import csv
import pandas


class Graph:
    def __init__(self, name):
        self.csv_name = name
        self.file_writer_dict = {}
        self.create_file_writer_dict()
        self.nodes = set()

    def create_file_writer_dict(self):
        for i in range(1, 10):
            file_writer = open(self.csv_name+str(i)+".csv", 'wt')
            file_writer.write("a,b\n")# header
            self.file_writer_dict[str(i)] = file_writer

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)

    def add_edge(self, x, y):
        if x < y:
            first_number = str(x)[:1]
            self.file_writer_dict[first_number].write(str(x)+","+str(y)+"\n")
        else:
            first_number = str(y)[:1]
            self.file_writer_dict[first_number].write(str(y)+","+str(x)+"\n")

    def number_of_edges(self):
        total_count = 0
        for i in range(1, 10):
            self.file_writer_dict[str(i)].close()
            data = pandas.read_csv(self.csv_name + str(i) + ".csv")
            data = data.drop_duplicates(subset=['a', 'b'], keep='first')
            rows, columns = data.shape
            total_count += rows
        return total_count

    def number_of_nodes(self):
        return len(self.nodes)

