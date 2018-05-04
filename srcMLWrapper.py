import subprocess
from ClassModel import *
from AttributeModel import *
from MethodModel import *
import os
import xml.etree.ElementTree as ET

class srcMLWrapper:
    def __init__(self, workingDir):
        self.workingDir = workingDir+"\~Temp"
        if not os.path.isdir(self.workingDir):
            os.mkdir(self.workingDir)

    def convertFiles(self, file):
            file_name = os.path.basename(file)
            file_xml = self.workingDir + "/"+file_name + ".xml"
            cmd = "srcml \""+file+"\" -o \""+file_xml+"\""

            rez = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            if rez:
                rez = "Converting "+file+" ...................\n"+str(rez)
            else:
                rez = "Converting " +file + " ...................\n"
            return rez, file_xml


    ###############################################################################################

    def getItem(self, item, name):
            return item.find("{http://www.srcML.org/srcML/src}"+name)

    def getItemName(self, item, name):
            new = item.find("{http://www.srcML.org/srcML/src}"+name)
            return self.getName(new)

    def getName(self, item):
        if item is not None:
            return self.getText(item.find("{http://www.srcML.org/srcML/src}name"))
        else:
            return "None"

    def getCallName(self, item):
        try:
            item = self.getItem(item, "name")
            names = item.findall("{http://www.srcML.org/srcML/src}name")
            var_name = self.getText(names[0])
            meth_name = self.getText(names[1])

            return var_name, meth_name
        except:
            return "None", "None"

    def getType(self, item):
        type = item.find("{http://www.srcML.org/srcML/src}type")
        name = self.getName(type)
        return name

    def getTypeAndName(self, item, tag):
        decl = item.find("{http://www.srcML.org/srcML/src}"+tag)
        type = self.getType(decl)
        name = self.getName(decl)

        return type, name

    def getAllItems(self, item, name):
        return item.findall("{http://www.srcML.org/srcML/src}"+name)

    def getText(self, atr):
        if atr is not None:
            text = atr.text
            if text is None:
                return self.getText(atr.find("{http://www.srcML.org/srcML/src}name"))
            text = text.replace(":", "")
            text = text.replace(" ", "")
            text = text.replace("\n", "")
            return text
        else:
            return "None"


    #############################################################################################

    def getAttributes(self, item, tag):
        attributes = []
        prev_type = "None"

        for decl in self.getAllItems(item, tag):
            for a in self.getAllItems(decl, "decl"):
                element_type = self.getType(a)
                if element_type == "None":
                    element_type = prev_type
                else:
                    prev_type = element_type

                element_name = self.getName(a)

                attribute = AttributeModel()
                attribute.setType(element_type)
                attribute.setName(element_name)

                attributes.append(attribute)

        return attributes

    def getMethods(self, item, tag, element_type):
        methods = []

        for decl in self.getAllItems(item, tag):
            element_name = self.getName(decl)
            if element_type == "java":
                specifier_item = self.getItem(decl, "specifier")
                element_type = self.getText(specifier_item)
            method = MethodModel()
            method.setType(element_type)
            method.setName(element_name)

            for param in self.getAttributes(self.getItem(decl, "parameter_list"), "parameter"):
                method.addArgs(param)
                method.addLocals(param)

            try:
                for param in self.getAttributes(self.getItem(decl, "block"), "decl_stmt"):
                    method.addLocals(param)
            except BaseException as e:
                print(e)


            try:
               for expr in self.getAllItems(self.getItem(decl, "block"), "expr_stmt"):
                    call = self.getItem(self.getItem(expr, "expr"), "call")
                    if call:
                        (var_name, var_method) = self.getCallName(call)
                        method.addCall(var_name)
            except BaseException as e:
                print(e)

            methods.append(method)

        return methods

    def getNamespaceRoot(self, root):
        item = root.find("{http://www.srcML.org/srcML/src}namespace")
        if item:
            root = item.find("{http://www.srcML.org/srcML/src}block")
            if root.find("{http://www.srcML.org/srcML/src}namespace"):
                return self.getNamespaceRoot(root)
        return root


    def getClassModelJava(self, file, root):
        classList = []

        for item in root.findall("{http://www.srcML.org/srcML/src}class"):
            insideClassList = self.getClassModelJava(file, item)
            if insideClassList:
                classList.extend(insideClassList)
            classModel = ClassModel()

            classModel.setFile(file)
            classModel.setName(self.getName(item))
            classModel.setSuperClass(self.getItemName(item, "super"))

            block = self.getItem(item, 'block')

            for attribute in self.getAttributes(block, "decl_stmt"):
                classModel.addAttribute(attribute)

            for method in self.getMethods(block, "function", "java"):
                classModel.addMethod(method)

            for method in self.getMethods(block, "constructor", "java"):
                classModel.addMethod(method)

            classList.append(classModel)

        return classList

    def getClassModelCpp(self, file):
        classList = []

        tree = ET.parse(file)
        root = tree.getroot()

        root = self.getNamespaceRoot(root)
        for item in root.findall("{http://www.srcML.org/srcML/src}class"):
            classModel = ClassModel()

            classModel.setFile(file)
            classModel.setName(self.getName(item))
            classModel.setSuperClass(self.getItemName(item, "super"))

            block = self.getItem(item, 'block')
            for atr in block:
                element_type = self.getText(atr)

                for attribute in self.getAttributes(atr, "decl_stmt"):
                    classModel.addAttribute(attribute)

                for method in self.getMethods(atr, "function_decl", element_type):
                    classModel.addMethod(method)

                for method in self.getMethods(atr, "constructor_decl", element_type):
                    classModel.addMethod(method)

                for method in self.getMethods(atr, "function", element_type):
                    classModel.addMethod(method)

            classList.append(classModel)

        return classList

    def getClassModel(self, file):
        classList = []
        import xml.etree.ElementTree as ET
        tree = ET.parse(file)
        root = tree.getroot()

        if file.endswith('.java.xml'):
            classList = self.getClassModelJava(file, root)
        else:
            classList = self.getClassModelCpp(file)

        return classList
