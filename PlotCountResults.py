from Graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import statistics


class PlotCountResults:
    def __init__(self, structure_manager):
        self.results_count = []
        for i in range(0, 4):
            self.results_count.append(-1)
        self.structure_manager = structure_manager
        self.proj_name = self.structure_manager.working_dir.replace("/~results", "").split("\\")[-1]
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        self.count_minus_code_and_git5_links()
        self.count_minus_code_and_git10_links()

        with open('E:\\results_graph.txt', 'a') as file:
            line = ",".join([str(x) for x in self.results_count])
            file.write(line + "\n")

        print(self.results_count)

    def count_minus_code_and_git5_links(self):
        g = Graph(self.working_dir + "\\minus_code_and_git5_links")
        x = []
        y = []
        max_val = []
        try:
            for classItem in self.structure_manager.get_class_list():
                classItem.get_median(classItem.git_links_below5, x, y, max_val)
        except BaseException as e:
            print(e)
        colors = (0, 0, 0)
        area = np.pi * 3

        max_val = list(set(max_val))
        med = statistics.mean(max_val)
        print(med)
        plt.clf()
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title(self.proj_name + " <5 cs")
        plt.xlabel('LD unique id')
        plt.ylabel('OCC')
        plt.axhline(y=med, color='b')
        plt.savefig("E:\\fig" + self.proj_name + "5.png")

        try:
            for classItem in self.structure_manager.get_class_list():
                related_list = classItem.get_git_links(classItem.git_links_below5, med)
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)

        self.results_count[0] = med
        self.results_count[1] = g.number_of_edges()

    def count_minus_code_and_git10_links(self):
        g = Graph(self.working_dir + "\\minus_code_and_git10_linkss")
        x = []
        y = []
        max_val = []
        try:
            for classItem in self.structure_manager.get_class_list():
                classItem.get_median(classItem.git_links_below10, x, y, max_val)
        except BaseException as e:
            print(e)

        max_val = list(set(max_val))
        med = statistics.mean(max_val)
        print(med)

        colors = (0, 0, 0)
        area = np.pi * 3
        plt.clf()
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title(self.proj_name + " <10 cs")
        plt.xlabel('LD unique id')
        plt.ylabel('OCC')
        plt.axhline(y=med, color='b')
        plt.savefig("E:\\fig"+self.proj_name+"10.png")

        try:
            for classItem in self.structure_manager.get_class_list():
                related_list = classItem.get_git_links(classItem.git_links_below10, med)
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)

        self.results_count[2] = med
        self.results_count[3] = g.number_of_edges()