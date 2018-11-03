from Graph import Graph


class Counter:
    def __init__(self, structureManager):
        self.resultsText = ""
        self.structureManager = structureManager

    def startCount(self):
        try:
            self.countCodeLinks()
            self.countGit5Links()
            self.countGit10Links()
            self.countGit20Links()
            self.countGitTotalLinks()
            self.countCodeAndGit5Links()
            self.countCodeAndGit10Links()
            self.countCodeAndGit20Links()
            self.countCodeAndTotalGitLinks()

            print(self.resultsText)
            self.saveResults()
        except BaseException as e:
            print(e)

    def saveResults(self):
        f = open("D:\\results.txt", "a+")
        f.write(self.resultsText+"\n")

    def countCodeLinks(self):
        print(".")
        g = Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getRelated()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        print("Number of classes: " + str(g.number_of_nodes()) + ",")
        self.resultsText += str(g.number_of_nodes()) + ","
        self.resultsText += str(g.number_of_edges()) + ","

    def countGit5Links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()

            try:
                for classItem in self.structureManager.getClassList():
                    className = classItem.name
                    g.add_node(classItem.name)
                    git_list = classItem.getOccurencesBelow5(occ)
                    for related in git_list:
                        g.add_edge(className, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countGit10Links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()

            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    git_list = classItem.getOccurencesBelow10(occ)
                    for related in git_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countGit20Links(self):
        print(".")
        for occ in range(1, 5):

            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    git_list = classItem.getOccurencesBelow20(occ)
                    for related in git_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countGitTotalLinks(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    git_list = classItem.getOccurrencesTotal(occ)
                    for related in git_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countCodeAndTotalGitLinks(self):
        print(".")

        for occ in range(1, 5):
            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    related_list = classItem.getMatchOccTotal(occ)
                    for related in related_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countCodeAndGit5Links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    related_list = classItem.getMatch5Occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countCodeAndGit10Links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    related_list = classItem.getMatch10Occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

    def countCodeAndGit20Links(self):
        print(".")
        for occ in range(1, 5):
            g = Graph()
            try:
                for classItem in self.structureManager.getClassList():
                    g.add_node(classItem.name)
                    related_list = classItem.getMatch20Occ(occ)
                    for related in related_list:
                        g.add_edge(classItem.name, related)
            except BaseException as e:
                print(e)
            self.resultsText += str(g.number_of_edges()) + ","

