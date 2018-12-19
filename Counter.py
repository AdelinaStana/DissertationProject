from Graph import Graph


class Counter:
    def __init__(self, structure_manager):
        self.results_text = ""
        self.structure_manager = structure_manager
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        try:
            self.count_code_links()
            self.count_git5_links()
            self.count_git10_links()
            self.count_git20_links()
            self.count_git_total_links()
            self.count_code_and_git5_links()
            self.count_code_and_git10_links()
            self.count_code_and_git20_links()
            self.count_code_and_total_git_links()

            print(self.results_text)
            self.save_results()
        except BaseException as e:
            print(e)

    def save_results(self):
        f = open("E:\\results.txt", "a+")
        f.write(self.results_text + "\n")

    def count_code_links(self):
        g = Graph(self.working_dir+"\\code_links.csv")
        try:
            for classItem in self.structure_manager.get_class_list():
                g.add_node(classItem.unique_id)
                related_list = classItem.get_related()
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)
        print("Number of classes: " + str(g.number_of_nodes()) + ",")
        self.results_text += str(g.number_of_nodes()) + ","
        self.results_text += str(g.number_of_edges()) + ","

    def count_git5_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git5_links.csv")

            try:
                for class_item in self.structure_manager.get_class_list():
                    git_list = class_item.get_occurrence_below5(occ)
                    for related in git_list:
                        g.add_edge(class_item.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_git10_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git10_links.csv")

            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrence_below10(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_git20_links(self):
        print(".")
        for occ in range(1, 5):

            g = Graph(self.working_dir+"\\git20_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrence_below20(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_git_total_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git_total_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrences_total(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_code_and_total_git_links(self):
        print(".")

        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git_total_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match_occ_total(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_code_and_git5_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git5_total_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match5_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_code_and_git10_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git10_total_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match10_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

    def count_code_and_git20_links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git20_total_links.csv")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match20_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_text += str(g.number_of_edges()) + ","

