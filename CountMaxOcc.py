from Graph import Graph
from threading import Thread


class CountMaxOcc:
    def __init__(self, structure_manager):
        self.results_count = []
        for i in range(0, 10):
            self.results_count.append(-1)
        self.structure_manager = structure_manager
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        import time

        start = time.time()
        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            t_git5 = Thread(target=self.count_git5_links, args=(2,))
            t_git10 = Thread(target=self.count_git10_links, args=(3,))
            t_git20 = Thread(target=self.count_git20_links, args=(4,))
            t_total = Thread(target=self.count_git_total_links, args=(5,))
            t_code_git5 = Thread(target=self.count_code_and_git5_links, args=(6,))
            t_code_git10 = Thread(target=self.count_code_and_git10_links, args=(7,))
            t_code_git20 = Thread(target=self.count_code_and_git20_links, args=(8,))
            t_code_git_total = Thread(target=self.count_code_and_total_git_links, args=(9,))

            t_code.start()
            t_git5.start()
            t_git10.start()
            t_git20.start()
            t_total.start()
            t_code_git5.start()
            t_code_git10.start()
            t_code_git20.start()
            t_code_git_total.start()

            threads.append(t_code)
            threads.append(t_git5)
            threads.append(t_git10)
            threads.append(t_git20)
            threads.append(t_total)
            threads.append(t_code_git5)
            threads.append(t_code_git10)
            threads.append(t_code_git20)
            threads.append(t_code_git_total)

            for t in threads:
                t.join()

            print(self.results_count)
            with open('E:\\results.txt', 'a') as file:
                line = ",".join([str(x) for x in self.results_count])
                file.write(line + "\n")
        except BaseException as e:
            print(e)
        end = time.time()

        elapsed = end - start
        print(elapsed)

    def count_code_links(self):
        g = Graph(self.working_dir+"\\code_links")
        try:
            for classItem in self.structure_manager.get_class_list():
                g.add_node(classItem.unique_id)
                related_list = classItem.get_related()
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)
        print("Number of classes: " + str(g.number_of_nodes()) + ",")
        self.results_count[0] = g.number_of_nodes()
        self.results_count[1] = g.number_of_edges()

    def count_git5_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\git5_links")
            try:
                for class_item in self.structure_manager.get_class_list():
                    git_list = class_item.get_occurrence_below5(occ)
                    for related in git_list:
                        g.add_edge(class_item.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count git5 links..."+str(nr))
        

    def count_git10_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\git10_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrence_below10(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1
        self.results_count[pos] = occ
        print("Count git10 links..."+str(nr))

    def count_git20_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\git20_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrence_below20(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count git20 links..."+str(nr))

    def count_git_total_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\git_total_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_occurrences_total(occ)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count git total links..."+str(nr))

    def count_code_and_total_git_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\code_git_total_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match_occ_total(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count code and total links..."+str(nr))

    def count_code_and_git5_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\code_git5_total_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match5_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count code and git5..."+str(nr))

    def count_code_and_git10_links(self, pos):
        occ = 1
        stop = True
        nr = []
        while stop:
            g = Graph(self.working_dir+"\\code_git10_total_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match10_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count code and git10..."+str(nr))

    def count_code_and_git20_links(self, pos):
        occ = 1
        stop = True
        nr =[]
        while stop:
            g = Graph(self.working_dir+"\\code_git20_total_links")
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_match20_occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            nr.append(g.number_of_edges())
            if g.number_of_edges() == 0:
                stop = False
            else:
                occ += 1

        self.results_count[pos] = occ
        print("Count code and git20..."+str(nr))

