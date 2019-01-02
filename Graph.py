import csv
import pandas


class Graph:
    def __init__(self, name):
        self.csv_name = name
        self.csv_dict = {}
        self.file_writer_dict = {}
        self.create_file_writer_dict()
        self.nodes = set()

    def create_file_writer_dict(self):
        for i in range(1, 10):
            self.csv_dict[str(i)] = open(self.csv_name+str(i)+".csv", 'wt')
            file_writer = csv.writer(self.csv_dict[str(i)], delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['a', 'b'])# header
            self.file_writer_dict[str(i)] = file_writer

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)

    def add_edge(self, x, y):
        if x < y:
            first_number = str(x)[:1]
            self.file_writer_dict[first_number].writerow([x, y])
        else:
            first_number = str(y)[:1]
            self.file_writer_dict[first_number].writerow([y, x])

    def number_of_edges(self):
        total_count = 0
        for i in range(1, 10):
            self.csv_dict[str(i)].close()
            data = pandas.read_csv(self.csv_name + str(i) + ".csv")
            data = data.drop_duplicates(subset=['a', 'b'], keep='first')
            rows, columns = data.shape
            total_count += rows
        return total_count

    def number_of_nodes(self):
        return len(self.nodes)

