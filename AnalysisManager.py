import re
import shutil

from GitWrapper import GitWrapper
from StructureManager import *
from SrcMLWrapper import SrcMLWrapper
from Counter import Counter
from PlotCountResults import PlotCountResults


class AnalysisManager:
    def __init__(self, parent, working_dir):
        self.parent = parent
        if os.path.isdir(working_dir):
            self.workingDir = working_dir
            try:
                os.mkdir(self.workingDir + "/~results")
            except:
                shutil.rmtree(self.workingDir + "/~results")
                os.mkdir(self.workingDir + "/~results")

            self.srcMLWrapper = SrcMLWrapper(self.workingDir)
            self.structureManager = StructureManager(self.workingDir)
        else:
            print("Cannot set "+working_dir+" as working directory!")

        self.filesList = []
        self.converted_files_list = []
        self.old_paths_dict = {}

    def get_git_commits(self):
        git_wrapper = GitWrapper(self.workingDir)
        git_wrapper.get_commits()

    def get_renamed_paths(self):
        git_wrapper = GitWrapper(self.workingDir)
        self.old_paths_dict = git_wrapper.get_old_paths(self.filesList)

    def assign_old_paths(self):
        for class_item in self.structureManager.class_list:
            try:
                path = class_item.rel_file_path
                class_item.set_old_paths(self.old_paths_dict[path])
            except BaseException as e:
                print("rel path not found!")

    def set_files_list(self, files):
        self.filesList = files

    def set_xml_files_list(self, files_dir):
        self.converted_files_list = []
        for r, d, f in os.walk(files_dir):
            for file in f:
                self.converted_files_list.append(os.path.join(r, file))

    def load_structure_from_xml(self, file):
        self.structureManager.loadStructure(file)

    def convert_to_xml(self):
        self.converted_files_list = []
        for file in self.filesList:
            if not re.search('\.xml', file):
                return_val, path_to_file = self.srcMLWrapper.convert_files(file)
                self.converted_files_list.append(path_to_file)
                self.parent.print_line(return_val)
            else:
                self.parent.print_line("Files already converted to XML!")
                break

    def remove_comments(self, string):
        string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                        string)  # remove all occurance streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("@@.*?@@", re.DOTALL), "",
                        string)
        string = re.sub(re.compile("//.*?\n"), "",
                        string)  # remove all occurance singleline comments (//COMMENT\n ) from string
        return string

    def remove_git_simbols(self, string):
        string = string.replace('+', '')
        string = string.replace('-', '')
        return string

    def build_git_model_with_comments(self):
        print("Start analysing git diffs...")
        for file in os.listdir(self.workingDir+"//~diffs"):
            try:
                datafile = open(self.workingDir+"//~diffs//"+file, 'r+', encoding="utf8", errors='ignore').read()
                file = file.replace('.txt', '')
                nr_of_commits_str = file.split('FilesChanged_')[1]
                commit_size = int(nr_of_commits_str)
                git_link_list = set()

                list_of_lines = datafile.split('\n')
                for index in range(0, len(list_of_lines)-1):
                    line = list_of_lines[index].strip()
                    if re.search("\+\+\+ b.*", line):
                        file_name = line.replace('+++ b', 'a')
                        file_name = file_name.strip()
                        if re.search('\.cs', file_name) or re.search('\.java', file_name):
                            git_link_list.add(file_name)

                if len(git_link_list) > 1:
                    self.structureManager.set_git_links_to_class(git_link_list, commit_size)
            except BaseException as e:
                print(e)

    def build_git_model_without_comments(self):
        print("Start analysing git diffs...")
        for file in os.listdir(self.workingDir+"//~diffs"):
            try:
                datafile = open(self.workingDir+"//~diffs//"+file, 'r+', encoding="utf8", errors='ignore').read()
                datafile = self.remove_comments(datafile)
                file = file.replace('.txt', '')
                nr_of_commits_str = file.split('FilesChanged_')[1]
                commit_size = int(nr_of_commits_str)
                git_link_list = set()
                temp_list = datafile.split('\n')
                list_of_lines = []
                for line in temp_list:
                    if not re.match('^\s*$', line):
                        list_of_lines.append(line)
                for index in range(0, len(list_of_lines)-1):
                    line = list_of_lines[index]

                    if re.search("\+\+\+ b.*", line):
                        file_name = line.replace('+++ b', 'a')
                        file_name = file_name.strip()
                        if not list_of_lines[index+1].startswith('diff'):
                            if re.search('\.cs', file_name) or re.search('\.java', file_name):
                                git_link_list.add(file_name)

                if len(git_link_list) > 1:
                    self.structureManager.set_git_links_to_class(git_link_list, commit_size)
            except BaseException as e:
                print(e)

    def analyse_xml(self):
        for file in self.converted_files_list:
            try:
                self.parent.print_line("Analysing " + file + " ...")
                class_list = self.srcMLWrapper.get_class_model(file)
                for classStructure in class_list:
                    self.structureManager.add_class(classStructure)
            except BaseException as e:
                print(e)

        self.structureManager.build_related()

    def process_data(self):
        print("Building structural dependencies!")
        self.analyse_xml()

        self.get_renamed_paths()
        self.assign_old_paths()

        print("Build git model!")
        self.build_git_model_with_comments()
        # self.structureManager.save_to_xml()
        print("Start counter!")
        counter = Counter(self.structureManager)
        counter.start_count()

        counter = PlotCountResults(self.structureManager)
        counter.start_count()

