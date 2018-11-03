class MethodModel:
    def __init__(self):
        self.type = "None"
        self.name = "None"
        self.args = []
        self.locals = []

    def setType(self, type):
        self.type = type

    def setName(self, name):
        self.name = name

    def addLocals(self, local):
        self.locals.append(local)

    def addCall(self, localName):
        for local in self.locals:
            if local.getName() == localName:
                local.addCall()

    def addArgs(self, arg):
        self.args.append(arg)

    def getArgs(self):
        return self.args

    def getLocals(self):
        return self.locals

    def getName(self):
        return self.name

    def getType(self):
        return self.type
