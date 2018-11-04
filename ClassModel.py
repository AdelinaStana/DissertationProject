import os


class ClassModel:
    def __init__(self, parent=None):
        self.parent = parent
        self.superclass = "None"
        self.name = "None"
        self.file = "None"
        self.attributes = set()
        self.methods = set()
        self.git_links_below5 = []
        self.git_links_below10 = []
        self.git_links_below20 = []
        self.git_links_total = []
        self.relation_list = set()

    def set_name(self, name):
        self.name = name

    def set_file(self, file):
        self.file = file.replace('.xml', '')

    def set_super_class(self, name):
        self.superclass = name

    def add_attribute(self, attrib):
        self.attributes.add(attrib)

    def add_method(self, meth):
        self.methods.add(meth)

    def get_super_class(self):
        return self.superclass

    def get_name(self):
        return self.name

    def get_file_path(self):
        return self.file

    def get_file_name(self):
        return os.path.basename(self.file)

    def get_attributes(self):
        return self.attributes

    def get_methods(self):
        return self.methods

    def set_related(self, rellist):
        self.relation_list = rellist

    def get_related(self):
        return self.relation_list

    def build_related(self, class_names_list):
        self.relation_list = set()

        for attrib in self.attributes:
            self.relation_list.add(attrib.get_type())

        for method in self.methods:
            for arg in method.get_args():
                self.relation_list.add(arg.get_type())

            for local in method.get_locals():
                self.relation_list.add(local.get_type())

        if self.superclass != "None":
            self.relation_list.add(self.superclass)

        self.relation_list = self.filter_known_classes(self.relation_list, class_names_list)

        return self

    def filter_known_classes(self, git_links, class_names_list):
        git_links_filtered = []
        for x in git_links:
            if x in class_names_list:
                git_links_filtered.append(x)

        return git_links_filtered

    def build_git(self, class_names_list):
        self.git_links_below5 = self.filter_known_classes(self.git_links_below5, class_names_list)
        self.git_links_below10 = self.filter_known_classes(self.git_links_below10, class_names_list)
        self.git_links_below20 = self.filter_known_classes(self.git_links_below20, class_names_list)
        self.git_links_total = self.filter_known_classes(self.git_links_total, class_names_list)

        return self

    def print_details(self, UIObj):
        UIObj.print_line("________________________________")
        UIObj.print_line("Class name: " + self.name)
        UIObj.print_line("Superclass: " + self.superclass)
        UIObj.print_line("Attributes: ")
        for attribute in self.attributes:
            UIObj.print_line("Type: " + attribute.get_type() + " Name: " + attribute.get_name())
        UIObj.print_line("Methods:")
        for method in self.methods:
            s = method.get_type() + ": " + method.get_name() + "("
            for arg in method.get_args():
                s = s + "Type: " + arg.get_type() + " Name: " + arg.get_name() + ","
            s += ")"
            UIObj.print_line(s)
            if method.get_locals():
                UIObj.print_line(" Local decl:")
                for local in method.get_locals():
                    UIObj.print_line(" Type: " + local.get_type() + " Name: " + local.get_name())

                UIObj.print_line(" Calls:")
                for local in method.get_locals():
                    if len(local.get_calls()) != 0:
                        UIObj.print_line(" Type: " + local.get_type() + " Name: " + local.get_name())
                        for call in local.get_calls():
                            UIObj.print_line(call)

    def set_git_links(self, links, nr_of_commits):
        for link in links:
            if link != self.name:
                if nr_of_commits <= 5:
                    self.git_links_below5.append(link)
                if nr_of_commits <= 10:
                    self.git_links_below10.append(link)
                if nr_of_commits <= 20:
                    self.git_links_below20.append(link)

                self.git_links_total.append(link)

    ##########################################################################################################

    def get_occurrence_below5(self, nr):
        return set([item for item in self.git_links_below5 if self.git_links_below5.count(item) >= nr])

    def get_occurrence_below10(self, nr):
        return set([item for item in self.git_links_below10 if self.git_links_below10.count(item) >= nr])

    def get_occurrence_below20(self, nr):
        return set([item for item in self.git_links_below20 if self.git_links_below20.count(item) >= nr])

    def get_occurrences_total(self, nr):
        links = self.get_git_links_total()
        return [item for item in links if links.count(item) >= nr]

    #########################################################################################################

    def get_git_links_total(self):
        return self.git_links_total

    def get_git5_links(self):
        return set(self.git_links_below5)

    def get_git10_links(self):
        return set(self.git_links_below10)

    def get_git20_links(self):
        return set(self.git_links_below20)

    #####################################################################################################

    def get_match5_occ(self, nr_of_occ):
        git_links = self.get_occurrence_below5(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def get_match10_occ(self, nr_of_occ):
        git_links = self.get_occurrence_below10(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def get_match20_occ(self, nr_of_occ):
        git_links = self.get_occurrence_below20(nr_of_occ)
        return set(self.relation_list).intersection(git_links)

    def get_match_occ_total(self, nr_of_occ):
        git_links = self.get_occurrences_total(nr_of_occ)
        return set(self.relation_list).intersection(git_links)




