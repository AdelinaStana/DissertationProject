import xml.etree.ElementTree as ET
from ClassModel import ClassModel
from AttributeModel import AttributeModel
from MethodModel import MethodModel
import os

class StructureManager:
    def __init__(self, workingDir):
        self.classlist = []
        self.classlistNames = []
        self.classlistFiles = []
        self.linksCount = {}
        self.workingDir = workingDir + "\~results"
        if not os.path.isdir(self.workingDir):
            os.mkdir(self.workingDir)

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
                classFile.text = classItem.getFilePath()

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

                gitLinksElement = ET.SubElement(classElement, 'gitlinksbelow5')
                gitList = ",".join(classItem.getGit5Links())
                gitLinksElement.text = gitList

                gitLinksElement = ET.SubElement(classElement, 'gitlinkbelow10')
                gitList = ",".join(classItem.getGit10Links())
                gitLinksElement.text = gitList

                gitLinksElement = ET.SubElement(classElement, 'gitlinkbelow20')
                gitList = ",".join(classItem.getGit20Links())
                gitLinksElement.text = gitList

                gitLinksElement = ET.SubElement(classElement, 'gitlinktotal')
                gitList = ",".join(classItem.getGitLinksTotal())
                gitLinksElement.text = gitList

                codeRelatedElement = ET.SubElement(classElement, 'codelinks')
                relatedList = ",".join(classItem.getRelated())
                codeRelatedElement.text = relatedList
            except BaseException as e:
                print(e)

        # create xml
        try:
            mydata = ET.tostring(data)
            myfile = open(self.workingDir+"\items_comm4.xml", "w+")
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
                    classModel.git_links_below5 = gitLinks5.split(',')

                gitLinks10 = self.getItemTextByName(item, "gitlinkbelow10")
                if gitLinks10:
                    classModel.git_links_below10 = gitLinks10.split(',')

                gitLinks20 = self.getItemTextByName(item, "gitlinkbelow20")
                if gitLinks20:
                    classModel.git_links_below20 = gitLinks20.split(',')

                gitLinksTotal = self.getItemTextByName(item, "gitlinktotal")
                if gitLinks20:
                    classModel.git_links_total = gitLinksTotal.split(',')

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
        self.classlistNames.append(classStruct.getName())
        self.classlistFiles.append(classStruct.getFilePath())

    def getClassList(self):
        return self.classlist

    def getRelated(self, className):
        try:
            return self.linksCount[className]
        except BaseException as e:
            print(e)

    def setGitLinksToClass(self, links, nrOfCommits):
        classLinks = []
        for classStruct in self.classlist:
            if classStruct.getFileName() in links:
                classLinks.append(classStruct.getName())

        try:
            for classStruct in self.classlist:
                if classStruct.getName() in classLinks:
                    classStruct.setGitLinks(classLinks, nrOfCommits)
        except BaseException as e:
            print(e)

    def buildRelated(self):
        for item in self.classlist:
            item = item.buildRelated(self.classlistNames)

    def buildGit(self):
        for classItem in self.classlist:
            self.classlistNames.append(classItem.getName())
        for item in self.classlist:
            item = item.buildGit(self.classlistNames)

