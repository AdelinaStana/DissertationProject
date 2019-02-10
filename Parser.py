from AttributeModel import *


class Parser:
    def __init__(self, root_dir, unique_id):
        self.working_dir = root_dir
        self.unique_id = unique_id

    def get_item(self, item, name):
        return item.find("{http://www.srcML.org/srcML/src}" + name)

    def get_item_name(self, item, name):
        new = item.find("{http://www.srcML.org/srcML/src}" + name)
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

    def get_type_and_name(self, item, tag):
        _decl = item.find("{http://www.srcML.org/srcML/src}" + tag)
        _type = self.get_type(_decl)
        name = self.get_name(_decl)

        return _type, name

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