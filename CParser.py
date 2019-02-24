from ClassModel import *
from MethodModel import *
import xml
from Parser import Parser
from AttributeModel import AttributeModel

class CParser(Parser):
    def __init__(self, root_dir, unique_id):
        Parser.__init__(self, root_dir, unique_id)

    def find_template_name_arg(self, item):
        items = item.iter()
        for it in items:
            if str(it.tag).endswith("name"):
                if it.find("{http://www.srcML.org/srcML/src}argument_list"):
                    return it.find("{http://www.srcML.org/srcML/src}argument_list")
        return item

    def get_type(self, item):
        _type = item.find("{http://www.srcML.org/srcML/src}type")
        name = self.get_name(_type)
        try:
            generic = self.find_template_name_arg(_type)
            if generic.tag != "{http://www.srcML.org/srcML/src}type":
                argument = generic.find("{http://www.srcML.org/srcML/src}argument")
                name = self.get_name(argument)
        except:
            pass
        return name

    def get_all_items(self, item, name):
        if str(item.tag).endswith(name):
            return [item]
        else:
            return item.findall("{http://www.srcML.org/srcML/src}" + name)

    def get_methods(self, item, tag):
        methods = []

        for decl in self.get_all_items(item, tag):
            element_name = self.get_name(decl)
            element_type = self.get_item_name(item, "type")

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
                pass

            try:
                for expr in self.get_all_items(self.get_item(decl, "block"), "expr_stmt"):
                    call = self.get_item(self.get_item(expr, "expr"), "call")
                    if call:
                        (var_name, var_method) = self.get_call_name(call)
                        method.add_call(var_name)
            except BaseException as e:
                pass

            methods.append(method)

        return methods

    def get_namespace_root(self, root):
        if root.find("{http://www.srcML.org/srcML/src}block"):
            root = root.find("{http://www.srcML.org/srcML/src}block")
        if root.find("{http://www.srcML.org/srcML/src}namespace"):
            return self.get_namespace_root(root)
        return root

    @staticmethod
    def get_namespaces(root):
        return root.findall("{http://www.srcML.org/srcML/src}namespace")

    def get_all(self, root):
        attributes = []
        names = root.iter("{http://www.srcML.org/srcML/src}name")
        for name in names:
            attribute = AttributeModel()
            t = self.get_text(name)
            attribute.set_type(t)
            attribute.set_name(t)

            attributes.append(attribute)
        return attributes

    def get_class_model(self, file, root):
        class_list = []

        if root.find("{http://www.srcML.org/srcML/src}block"):
            root = root.find("{http://www.srcML.org/srcML/src}block")

        item_list = root.findall("{http://www.srcML.org/srcML/src}class") + \
                    root.findall("{http://www.srcML.org/srcML/src}struct") + \
                    root.findall("{http://www.srcML.org/srcML/src}enum") + \
                    root.findall("{http://www.srcML.org/srcML/src}interface")

        for item in item_list:
            inside_class_list = self.get_class_model(file, item)

            if inside_class_list:
                class_list.extend(inside_class_list)

            class_model = ClassModel()
            self.unique_id += 1

            file_path = file.replace(self.working_dir, 'a/')
            file_path = file_path.replace(".xml", "")
            file_path = file_path.replace("\\", "/")

            class_model.set_file(file_path)
            class_model.set_unique_id(self.unique_id)
            class_model.set_name(self.get_name(item))
            class_model.set_super_class(self.get_item_name(item, "super"))
            # workaround
            for attribute in self.get_all(item):
                class_model.add_attribute(attribute)

            block = self.get_item(item, 'block')
            for atr in block:
                for attribute in self.get_attributes(atr, "decl_stmt"):
                    class_model.add_attribute(attribute)

                for method in self.get_methods(atr, "function_decl"):
                    class_model.add_method(method)

                for method in self.get_methods(atr, "constructor_decl"):
                    class_model.add_method(method)

                for method in self.get_methods(atr, "function"):
                    class_model.add_method(method)

            class_list.append(class_model)
        return class_list

    def get_class_list(self, file):
        class_list = []
        tree = xml.etree.ElementTree.parse(file)
        root = tree.getroot()

        namespace_list = self.get_namespaces(root)
        if len(namespace_list) > 0:
            for root_item in namespace_list:
                class_list += self.get_class_model(file, root_item)

        item_list = root.findall("{http://www.srcML.org/srcML/src}class") + \
                    root.findall("{http://www.srcML.org/srcML/src}struct") + \
                    root.findall("{http://www.srcML.org/srcML/src}enum") + \
                    root.findall("{http://www.srcML.org/srcML/src}interface")

        for item in item_list:
            class_list += self.get_class_model(file, item)

        return class_list
