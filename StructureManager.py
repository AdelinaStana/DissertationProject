import xml.etree.ElementTree as ET
from ClassModel import ClassModel
from AttributeModel import AttributeModel
from MethodModel import MethodModel


class StructureManager:
    def __init__(self, workingDir):
        self.classlist = []
        self.linksCount = {}
        self.workingDir = workingDir + "\~results"

    def saveToXml(self):
        data = ET.Element('data')
        for classItem in self.classlist:
            try:
                classElement = ET.SubElement(data, 'class')
                #add class details
                className = ET.SubElement(classElement, 'name')
                className.text = classItem.getName()
                superclass = ET.SubElement(classElement, 'superclass')
                superclass.text = classItem.getSuperClass()
                classFile = ET.SubElement(classElement, 'file')
                classFile.text = classItem.getFile()

                #add attributes
                attribElement = ET.SubElement(classElement, 'attributes')
                for attribItem in classItem.getAttributes():
                    attrib = ET.SubElement(attribElement, 'attribute')
                    attribName = ET.SubElement(attrib, 'name')
                    attribName.text = attribItem.getName()
                    attribType = ET.SubElement(attrib, 'type')
                    attribType.text = attribItem.getType()
                    attribCall = ET.SubElement(attrib, 'calls')
                    attribCall.text = attribItem.getCalls()

                methodElement = ET.SubElement(classElement, 'methods')
                for methodItem in classItem.getMethods():
                    method = ET.SubElement(methodElement, 'method')
                    methodName = ET.SubElement(method, 'name')
                    methodName.text = methodItem.getName()
                    methodType = ET.SubElement(method, 'type')
                    methodType.text = methodItem.getType()

                    localsElement = ET.SubElement(method, 'locals')
                    for attribItem in methodItem.getLocals():
                        local = ET.SubElement(localsElement, 'attribute')
                        attribName = ET.SubElement(local, 'name')
                        attribName.text = attribItem.getName()
                        attribType = ET.SubElement(local, 'type')
                        attribType.text = attribItem.getType()
                        attribCall = ET.SubElement(local, 'calls')
                        attribCall.text = str(attribItem.getCalls())

                gitLinks5, gitLinks20, gitLinks50 = classItem.getGitLinks()
                gitLinksElement = ET.SubElement(classElement, 'gitlinksbelow5')
                gitList = ",".join(gitLinks5)
                gitLinksElement.text = gitList

                gitLinksElement = ET.SubElement(classElement, 'gitlinksmore5below20')
                gitList = ",".join(gitLinks20)
                gitLinksElement.text = gitList

                gitLinksElement = ET.SubElement(classElement, 'gitlinksmore20')
                gitList = ",".join(gitLinks50)
                gitLinksElement.text = gitList

                codeRelatedElement = ET.SubElement(classElement, 'codelinks')
                relatedList = ",".join(classItem.getRelated())
                codeRelatedElement.text = relatedList
            except BaseException as e:
                print(e)

        # create xml
        try:
            mydata = ET.tostring(data)
            myfile = open(self.workingDir+"\items.xml", "w+")
            myfile.write(mydata.decode("utf-8"))
        except BaseException as e:
            print(e)

    def loadStructure(self, file):
        import xml.etree.ElementTree as ET
        tree = ET.parse(file)
        root = tree.getroot()

        try:

            for item in root.findall("class"):
                classModel = ClassModel()

                classModel.setFile(self.getItemTextByName(item, "file"))
                classModel.setName(self.getItemTextByName(item, "name"))
                classModel.setSuperClass(self.getItemTextByName(item, "super"))

                attributesItem = self.getItemByName(item, "attributes")
                if attributesItem:
                    for attrib in attributesItem.findall("attribute"):
                        attributeModel = AttributeModel()
                        attributeModel.setType(self.getItemTextByName(attrib, "name"))
                        attributeModel.setName(self.getItemTextByName(attrib, "type"))
                        calls = self.getItemTextByName(attrib, "calls")
                        if calls is not None:
                            attributeModel.setCalls(int(calls))
                        else:
                            attributeModel.setCalls(0)
                        classModel.addAttribute(attributeModel)

                methodsItem = self.getItemByName(item, "methods")
                if methodsItem:
                    for method in methodsItem.findall("method"):
                        methodModel = MethodModel()

                        methodModel.setType(self.getItemTextByName(method, "name"))
                        methodModel.setName(self.getItemTextByName(method, "type"))

                        localsItem = self.getItemByName(method, "locals")
                        if localsItem:
                            for attrib in localsItem.findall("attribute"):
                                attributeModel = AttributeModel()
                                attributeModel.setType(self.getItemTextByName(attrib, "name"))
                                attributeModel.setName(self.getItemTextByName(attrib, "type"))
                                calls = self.getItemTextByName(attrib, "calls")
                                if calls is not None:
                                    attributeModel.setCalls(int(calls))
                                else:
                                    attributeModel.setCalls(0)
                                methodModel.addLocals(attributeModel)

                        classModel.addMethod(methodModel)

                gitLinks5 = self.getItemTextByName(item, "gitlinksbelow5")
                if gitLinks5:
                    classModel.setGitLinks(gitLinks5.split(','),5)

                gitLinks20 = self.getItemTextByName(item, "gitlinksmore5below20")
                if gitLinks20:
                    classModel.setGitLinks(gitLinks20.split(','), 20)

                gitLinks = self.getItemTextByName(item, "gitlinksmore20")
                if gitLinks:
                    classModel.setGitLinks(gitLinks.split(','), 50)

                codeLinks = self.getItemTextByName(item, "codelinks")
                if codeLinks:
                    classModel.setRelated(codeLinks.split(','))

                self.classlist.append(classModel)
        except BaseException as e:
            print(e)

    def getText(self, atr):
        if atr is not None:
            text = atr.text
            return text
        else:
            return "None"

    def getItemByName(self, item, name):
            new = item.find(name)
            return new

    def getItemTextByName(self, item, name):
            new = item.find(name)
            return self.getText(new)

    def addClass(self, classStruct):
        self.classlist.append(classStruct)

    def getClassList(self):
        return self.classlist

    def getRelated(self, className):
        try:
            return self.linksCount[className]
        except BaseException:
            return 0

    def setGitLinksToClass(self, className, links, nrOfCommits):
        flag = False
        try:
            for classStruct in self.classlist:
                if classStruct.getName() == className:
                    flag = True
                    classStruct.setGitLinks(links, nrOfCommits)
            if not flag:
                print("Class: " + className+" not found!")
        except BaseException:
            return 0

    def buildRelated(self):

        for item in self.classlist:
            className = item.name
            counter = 0

            for other in self.classlist:
                if other.name != className:
                    relatedItems = other.getRelated()
                    print(className+"-------")
                    print(relatedItems)
                    if className in relatedItems:
                        counter += 1

            self.linksCount[className] = counter

