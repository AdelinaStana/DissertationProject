
class ClassModel():
    def __init__(self, parent=None):
        self.parent = parent
        self.superclass = "None"
        self.name = "None"
        self.file = "None"
        self.attributes = []
        self.methods = []
        self.git_links_below5 = []
        self.git_links_below20 = []
        self.git_links_more = []
        self.relation_list = []
        self.ignore_list = ['int', 'float', 'String', 'long', 'boolean','TreeNode', ]

    def setGitLinks(self, links, nrOfCommits):
        for link in links:
            if link != self.name:
                if nrOfCommits <= 5:
                    self.git_links_below5.append(link)
                if 5 < nrOfCommits <= 20:
                    self.git_links_below20.append(link)
                if nrOfCommits > 20:
                    self.git_links_more.append(link)

    def getGitLinks(self):
        return self.git_links_below5, self.git_links_below20, self.git_links_more

    def getGitLinksTotal(self):
        gitLinks = []
        gitLinks.extend(self.git_links_below5)
        gitLinks.extend(self.git_links_below20)
        gitLinks.extend(self.git_links_more)
        return gitLinks

    def setName(self, name):
        self.name = name

    def setFile(self, file):
        self.file = file

    def setSuperClass(self, name):
        self.superclass = name

    def addAttribute(self, attrib):
        self.attributes.append(attrib)

    def addMethod(self, meth):
        self.methods.append(meth)

    def getSuperClass(self):
        return self.superclass

    def getName(self):
        return self.name

    def getFile(self):
        return self.file

    def getAttributes(self):
        return self.attributes

    def getMethods(self):
        return self.methods

    def getMatch(self):
        git_links = self.getGitLinksTotal()
        return set(self.relation_list) & set(git_links)

    def setRelated(self, rellist):
        self.relation_list = rellist

    def getRelated(self):
        return self.relation_list

    def buildRelated(self):
        self.relation_list = []
        for method in self.methods:
            for arg in method.getArgs():
                self.relation_list.append(arg.getType())

            for local in method.getLocals():
                self.relation_list.append(local.getType())

        if self.superclass != "None":
            self.relation_list.append(self.superclass)

        self.relation_list = [x for x in self.relation_list if x not in self.ignore_list]

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



