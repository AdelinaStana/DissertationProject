from ClassModel import *
import xml
from Parser import Parser
from AttributeModel import AttributeModel


class NameTagParser(Parser):
    def __init__(self, root_dir, unique_id):
        Parser.__init__(self, root_dir, unique_id)

    def get_all_structures(self, root):
        item_list = []
        cls = root.iter("{http://www.srcML.org/srcML/src}class")
        for item in cls:
            item_list.append(item)
        cls = root.iter("{http://www.srcML.org/srcML/src}interface")
        for item in cls:
            item_list.append(item)
        return item_list

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

    def get_class_model(self, file, item_list):
        class_list = []

        for item in item_list:
            class_model = ClassModel()
            class_model.set_name(self.get_name(item))

            if class_model.name != "None":
                self.unique_id += 1

                file_path = file.replace(self.working_dir, 'a/')
                file_path = file_path.replace(".xml", "")
                file_path = file_path.replace("\\", "/")

                class_model.set_file(file_path)
                class_model.set_unique_id(self.unique_id)
                class_model.set_super_class(self.get_item_name(item, "super"))

                # workaround
                for attribute in self.get_all(item):
                    class_model.add_attribute(attribute)

                class_list.append(class_model)

        return class_list

    def get_class_list(self, file):
        tree = xml.etree.ElementTree.parse(file)
        root = tree.getroot()

        item_list = self.get_all_structures(root)
        class_list = self.get_class_model(file, item_list)

        return class_list
