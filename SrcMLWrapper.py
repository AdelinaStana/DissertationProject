import subprocess
import os
from JavaParser import JavaParser
from CParser import CParser
from NameTagParser import NameTagParser

class SrcMLWrapper:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.working_dir = root_dir + "/~Temp/"
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)
        self.unique_id = 0

    def convert_files(self, file):
        file_path = file.replace(self.root_dir, self.working_dir)
        file = file.replace("\\", "/")
        file = file.replace("//", "/")
        file_xml = file_path + ".xml"
        file_xml = file_xml.replace("\\", "/")
        file_xml = file_xml.replace("//", "/")
        dir_path = os.path.dirname(file_xml)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        cmd = "srcml \"" + file + "\" -o \"" + file_xml + "\""
        rez = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        if rez:
            rez = str(rez)
        else:
            rez = "Converting " + file + " ...................\n"
        return rez, file_xml

    def get_class_model(self, file):
        if file.endswith('.java.xml'):
            parser = NameTagParser(self.working_dir, self.unique_id)
            class_list = parser.get_class_list(file)
            self.unique_id = parser.unique_id
        else:
            parser = NameTagParser(self.working_dir, self.unique_id)
            class_list = parser.get_class_list(file)
            self.unique_id = parser.unique_id
        return class_list
