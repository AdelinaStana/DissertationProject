from ClassModel import *
from MethodModel import *
import xml
from Parser import Parser


class JavaParser(Parser):
    def __init__(self, root_dir, unique_id):
            Parser.__init__(self, root_dir, unique_id)

    def get_type(self, item):
        _type = item.find("{http://www.srcML.org/srcML/src}type")
        name = self.get_name(_type)
        return name

    def get_all_items(self, item, name):
        return item.findall("{http://www.srcML.org/srcML/src}" + name)

    def get_methods(self, item, tag):
        methods = []

        for decl in self.get_all_items(item, tag):
            element_name = self.get_name(decl)

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

    def get_class_model(self, file, root):
        class_list = []

        if root.find("{http://www.srcML.org/srcML/src}block"):
            root = root.find("{http://www.srcML.org/srcML/src}block")

        item_list = root.findall("{http://www.srcML.org/srcML/src}class") + \
                    root.findall("{http://www.srcML.org/srcML/src}interface")

        for item in item_list:
            class_name = self.get_name(item)
            inside_class_list = self.get_class_model(file, item)

            if inside_class_list:
                class_list.extend(inside_class_list)

            class_model = ClassModel()
            self.unique_id += 1

            file_path = file.replace(self.working_dir, 'a/')
            file_path = file_path.replace(".xml", "")
            file_path = file_path.replace("\\", "/")

            class_model.set_file(file_path)
            class_model.set_name(class_name)
            class_model.set_unique_id(self.unique_id)
            class_model.set_super_class(self.get_item_name(item, "super"))

            block = self.get_item(item, 'block')

            for attribute in self.get_attributes(block, "decl_stmt"):
                class_model.add_attribute(attribute)

            for method in self.get_methods(block, "function"):
                class_model.add_method(method)

            for method in self.get_methods(block, "constructor"):
                class_model.add_method(method)

            class_list.append(class_model)
        return class_list

    def get_class_list(self, file):
        class_list = []
        tree = xml.etree.ElementTree.parse(file)
        root = tree.getroot()

        if root:
            class_list = self.get_class_model(file, root)

        return class_list
