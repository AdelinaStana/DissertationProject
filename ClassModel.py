import os


class ClassModel:
    def __init__(self, parent=None):
        self.parent = parent
        self.superclass = "None"
        self.name = "None"
        self.file = "None"
        self.attributes = set()
        self.methods = set()
        self.git_links_below5 = []
        self.git_links_below10 = []
        self.git_links_below20 = []
        self.git_links_total = []
        self.relation_list = set()

    def setName(self, name):
        self.name = name

    def setFile(self, file):
        self.file = file.replace('.xml', '')

    def setSuperClass(self, name):
        self.superclass = name

    def addAttribute(self, attrib):
        self.attributes.add(attrib)

    def addMethod(self, meth):
        self.methods.add(meth)

    def getSuperClass(self):
        return self.superclass

    def getName(self):
        return self.name

    def getFilePath(self):
        return self.file

    def getFileName(self):
        return os.path.basename(self.file)

    def getAttributes(self):
        return self.attributes

    def getMethods(self):
        return self.methods

    def setRelated(self, rellist):
        self.relation_list = rellist

    def getRelated(self):
        return self.relation_list

    def buildRelated(self, classNamesList):
        self.relation_list = set()

        for attrib in self.attributes:
            self.relation_list.add(attrib.getType())

        for method in self.methods:
            for arg in method.getArgs():
                self.relation_list.add(arg.getType())

            for local in method.getLocals():
                self.relation_list.add(local.getType())

        if self.superclass != "None":
            self.relation_list.add(self.superclass)

        self.relation_list = self.filterKnownClasses(self.relation_list, classNamesList)

        return self

    def filterKnownClasses(self, gitLinks, classNamesList):
        gitLinksFiltered = []
        for x in gitLinks:
            if x in classNamesList:
                gitLinksFiltered.append(x)

        return gitLinksFiltered

    def buildGit(self, classNamesList):
        self.git_links_below5 = self.filterKnownClasses(self.git_links_below5, classNamesList)
        self.git_links_below10 = self.filterKnownClasses(self.git_links_below10, classNamesList)
        self.git_links_below20 = self.filterKnownClasses(self.git_links_below20, classNamesList)
        self.git_links_total = self.filterKnownClasses(self.git_links_total, classNamesList)

        return self

    def printDetails(self, UIObj):
        UIObj.printLine("________________________________")
        UIObj.printLine("Class name: " + self.name)
        UIObj.printLine("Superclass: " + self.superclass)
        UIObj.printLine("Attributes: ")
        for attribute in self.attributes:
            UIObj.printLine("Type: " + attribute.getType() + " Name: " + attribute.getName())
        UIObj.printLine("Methods:")
        for method in self.methods:
            s = method.getType()+": "+method.getName()+"("
            for arg in method.getArgs():
                s = s +"Type: " + arg.getType() + " Name: " + arg.getName()+","
            s += ")"
            UIObj.printLine(s)
            if method.getLocals():
                UIObj.printLine(" Local decl:")
                for local in method.getLocals():
                    UIObj.printLine(" Type: " + local.getType() + " Name: " + local.getName())

                UIObj.printLine(" Calls:")
                for local in method.getLocals():
                    if len(local.getCalls()) != 0:
                        UIObj.printLine(" Type: " + local.getType() + " Name: " + local.getName())
                        for call in local.getCalls():
                            UIObj.printLine(call)

    def setGitLinks(self, links, nrOfCommits):
        for link in links:
            if link != self.name:
                if nrOfCommits <= 5:
                    self.git_links_below5.append(link)
                if nrOfCommits <= 10:
                    self.git_links_below10.append(link)
                if nrOfCommits <= 20:
                    self.git_links_below20.append(link)

                self.git_links_total.append(link)

    ##########################################################################################################

    def getOccurencesBelow5(self, nr):
        return set([item for item in self.git_links_below5 if self.git_links_below5.count(item) >= nr])

    def getOccurencesBelow10(self, nr):
        return set([item for item in self.git_links_below10 if self.git_links_below10.count(item) >= nr])

    def getOccurencesBelow20(self, nr):
        return set([item for item in self.git_links_below20 if self.git_links_below20.count(item) >= nr])

    def getOccurrencesTotal(self, nr):
        links = self.getGitLinksTotal()
        return [item for item in links if links.count(item) >= nr]

    #########################################################################################################

    def getGitLinksTotal(self):
        return self.git_links_total

    def getGit5Links(self):
        return set(self.git_links_below5)

    def getGit10Links(self):
        return set(self.git_links_below10)

    def getGit20Links(self):
        return set(self.git_links_below20)

    #######################################################################################################

    def getMatch5(self):
        return set(self.relation_list).intersection(self.git_links_below5)

    def getMatch10(self):
        return set(self.relation_list).intersection(self.git_links_below10)

    def getMatch20(self):
        return set(self.relation_list).intersection(self.git_links_below20)

    def getMatchTotal(self):
        git_links = self.getGitLinksTotal()
        return set(self.relation_list).intersection(git_links)

    #####################################################################################################

    def getMatch5Occ(self, nr_of_occ):
        git_links = self.getOccurencesBelow5(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def getMatch10Occ(self, nr_of_occ):
        git_links = self.getOccurencesBelow10(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def getMatch20Occ(self, nr_of_occ):
        git_links = self.getOccurencesBelow20(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def getMatchOccTotal(self, nr_of_occ):
        git_links = self.getOccurrencesTotal(nr_of_occ)
        return set(self.relation_list).intersection(git_links)




