import subprocess
from ClassModel import *
from AttributeModel import *
from MethodModel import *
import os
import xml.etree.ElementTree as ET


class SrcMLWrapper:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.working_dir = root_dir + "/~Temp/"
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)
        '''else:
            shutil.rmtree(self.workingDir)
            os.mkdir(self.workingDir)'''

    def convert_files(self, file):
            file_path = file.replace(self.root_dir, self.working_dir)
            file_xml = file_path+".xml"
            dir_path = os.path.dirname(file_xml)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            cmd = "srcml \""+file+"\" -o \""+file_xml+"\""
            rez = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            if rez:
                rez = "Converting "+file+" ...................\n"+str(rez)
            else:
                rez = "Converting " +file + " ...................\n"
            return rez, file_xml


    ###############################################################################################

    def get_item(self, item, name):
            return item.find("{http://www.srcML.org/srcML/src}"+name)

    def get_item_name(self, item, name):
            new = item.find("{http://www.srcML.org/srcML/src}"+name)
            return self.get_name(new)

    def get_name(self, item):
        if item is not None:
            return self.get_text(item.find("{http://www.srcML.org/srcML/src}name"))
        else:
            return "None"

    def get_call_name(self, item):
        try:
            item = self.get_item(item, "name")
            names = item.findall("{http://www.srcML.org/srcML/src}name")
            var_name = self.get_text(names[0])
            meth_name = self.get_text(names[1])

            return var_name, meth_name
        except:
            return "None", "None"

    def get_type(self, item):
        _type = item.find("{http://www.srcML.org/srcML/src}type")
        name = self.get_name(_type)
        return name

    def get_type_and_name(self, item, tag):
        _decl = item.find("{http://www.srcML.org/srcML/src}"+tag)
        _type = self.get_type(_decl)
        name = self.get_name(_decl)

        return _type, name

    def get_all_items(self, item, name):
        return item.findall("{http://www.srcML.org/srcML/src}"+name)

    def get_text(self, atr):
        if atr is not None:
            text = atr.text
            if text is None:
                return self.get_text(atr.find("{http://www.srcML.org/srcML/src}name"))
            text = text.replace(":", "")
            text = text.replace(" ", "")
            text = text.replace("\n", "")
            return text
        else:
            return "None"


    #############################################################################################

    def get_attributes(self, item, tag):
        attributes = []
        prev_type = "None"

        for decl in self.get_all_items(item, tag):
            for a in self.get_all_items(decl, "decl"):
                element_type = self.get_type(a)
                if element_type == "None":
                    element_type = prev_type
                else:
                    prev_type = element_type

                element_name = self.get_name(a)

                attribute = AttributeModel()
                attribute.set_type(element_type)
                attribute.set_name(element_name)

                attributes.append(attribute)

        return attributes

    def get_methods(self, item, tag, element_type):
        methods = []

        for decl in self.get_all_items(item, tag):
            element_name = self.get_name(decl)
            if element_type == "java":
                specifier_item = self.get_item(decl, "specifier")
                element_type = self.get_text(specifier_item)
            method = MethodModel()
            method.set_type(element_type)
            method.set_name(element_name)

            for param in self.get_attributes(self.get_item(decl, "parameter_list"), "parameter"):
                method.add_args(param)
                method.add_locals(param)

            try:
                for param in self.get_attributes(self.get_item(decl, "block"), "decl_stmt"):
                    method.add_locals(param)
            except BaseException as e:
                print(e)

            try:
                for expr in self.get_all_items(self.get_item(decl, "block"), "expr_stmt"):
                    call = self.get_item(self.get_item(expr, "expr"), "call")
                    if call:
                        (var_name, var_method) = self.get_call_name(call)
                        method.add_call(var_name)
            except BaseException as e:
                print(e)

            methods.append(method)

        return methods

    def get_namespace_root(self, root):
        item = root.find("{http://www.srcML.org/srcML/src}namespace")
        if item:
            root = item.find("{http://www.srcML.org/srcML/src}block")
            if root.find("{http://www.srcML.org/srcML/src}namespace"):
                return self.get_namespace_root(root)
        return root

    def get_class_model_java(self, file, root):
        class_list = []

        if root.find("{http://www.srcML.org/srcML/src}block"):
            root = root.find("{http://www.srcML.org/srcML/src}block")

        for item in root.findall("{http://www.srcML.org/srcML/src}class"):
            class_name = self.get_name(item)
            inside_class_list = self.get_class_model_java(file, item)

            if inside_class_list:
                class_list.extend(inside_class_list)

            class_model = ClassModel()

            file_path = file.replace(self.working_dir, 'a/')
            file_path = file_path.replace(".xml", "")
            file_path = file_path.replace("\\", "/")

            class_model.set_file(file_path)
            class_model.set_name(class_name)
            class_model.set_super_class(self.get_item_name(item, "super"))

            block = self.get_item(item, 'block')

            for attribute in self.get_attributes(block, "decl_stmt"):
                class_model.add_attribute(attribute)

            for method in self.get_methods(block, "function", "java"):
                class_model.add_method(method)

            for method in self.get_methods(block, "constructor", "java"):
                class_model.add_method(method)

            class_list.append(class_model)
        return class_list

    def get_class_model_cpp(self, file):
        class_list = []

        tree = ET.parse(file)
        root = tree.getroot()

        root = self.get_namespace_root(root)
        for item in root.findall("{http://www.srcML.org/srcML/src}class"):
            class_model = ClassModel()

            class_model.set_file(file)
            class_model.set_name(self.get_name(item))
            class_model.set_super_class(self.get_item_name(item, "super"))

            block = self.get_item(item, 'block')
            for atr in block:
                element_type = self.get_text(atr)

                for attribute in self.get_attributes(atr, "decl_stmt"):
                    class_model.add_attribute(attribute)

                for method in self.get_methods(atr, "function_decl", element_type):
                    class_model.add_method(method)

                for method in self.get_methods(atr, "constructor_decl", element_type):
                    class_model.add_method(method)

                for method in self.get_methods(atr, "function", element_type):
                    class_model.add_method(method)

            class_list.append(class_model)
        return class_list

    def get_class_model(self, file):
        class_list = []
        import xml.etree.ElementTree as ET
        tree = ET.parse(file)
        root = tree.getroot()

        if file.endswith('.java.xml'):
            class_list = self.get_class_model_java(file, root)
        else:
            class_list = self.get_class_model_cpp(file)

        return class_list
