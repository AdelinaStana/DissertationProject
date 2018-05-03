class AttributeModel:
    def __init__(self, parent=None):
        self.type = "None"
        self.name = "None"
        self.calls = 0

    def setType(self, type):
        self.type = type

    def setName(self, name):
        self.name = name

    def addCall(self):
        self.calls+=1

    def setCalls(self, calls):
        self.calls = calls

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getCalls(self):
        return self.calls