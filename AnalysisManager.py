import re
import shutil

from GitWrapper import GitWrapper
from StructureManager import *
from srcMLWrapper import srcMLWrapper
from Counter import Counter


class AnalysisManager:
    def __init__(self, parent, workingDir):
        self.parent = parent
        if os.path.isdir(workingDir):
            self.workingDir = workingDir
            try:
                os.mkdir(self.workingDir + "\~results")
            except BaseException:
                shutil.rmtree(self.workingDir + "\~results")
                os.mkdir(self.workingDir + "\~results")

            self.srcMLWrapper = srcMLWrapper(self.workingDir)
            self.structureManager = StructureManager(self.workingDir)
        else:
            print("Cannot set "+workingDir+" as working directory!")

        self.filesList = []
        self.convertedFilesList = []
        self.resultsText = ""

    def getGitCommits(self):
        gitWrapper = GitWrapper(self.workingDir)
        gitWrapper.getRepo()

    def setFilesList(self, filesList):
        self.filesList = filesList

    def setXMLFilesList(self, filesDir):
        self.convertedFilesList = []
        for r, d, f in os.walk(filesDir):
            for file in f:
                self.convertedFilesList.append(os.path.join(r, file))

    def loadStructureFromXML(self, file):
        self.structureManager.loadStructure(file)
        self.buildModel()

    def convertToXML(self):
        self.convertedFilesList = []
        for file in self.filesList:
            if not re.search('\.xml', file):
                returnVal, pathToFile = self.srcMLWrapper.convertFiles(file)
                self.convertedFilesList.append(pathToFile)
                self.parent.printLine(returnVal)
            else:
                self.parent.printLine("Files already converted to XML!")
                break

    def removeComments(self, string):
        string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                        string)  # remove all occurance streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("//.*?\n"), "",
                        string)  # remove all occurance singleline comments (//COMMENT\n ) from string
        return string

    def removeGitSimbols(self, string):
        string = string.replace('+', '')
        string = string.replace('-', '')
        return string

    def buldGitModel(self):
        print("Start analysing git diffs...")
        for file in os.listdir(self.workingDir+"//~diffs"):
            try:
                print(file)
                datafile = open(self.workingDir+"//~diffs//"+file, 'r+', encoding="utf8", errors='ignore').read()
                #datafile = self.removeComments(datafile)
                #datafile = self.removeGitSimbols(datafile)
                file = file.replace('.txt', '')
                nrOfCommitsStr = file.split('FilesChanged_')[1]
                nrOfCommits = int(nrOfCommitsStr)
                git_link_list = set()
                tempList = datafile.split('\n')
                listOfLines = []
                for line in tempList:
                    if line.strip() != '':
                        listOfLines.append(line)
                for index in range(0, len(listOfLines)-1):
                    line = listOfLines[index]
                    '''if re.search('.*::.*\{', line):
                        words = line.split(' ')
                        for i in range(0, len(words)):
                            word = words[i]
                            if re.search('.*::.*', word):
                                name = word.split('::')
                                if name not in git_link_list:
                                    git_link_list.append(name[0])'''

                    if re.search('.*class .*', line) or re.search('.*public class .*', line) or re.search('.*private class .*', line):
                        try:
                            words = line.split(' ')
                            for i in range(0, len(words)):
                                word = words[i].strip()
                                if word == 'class' and words[i + 1].strip() not in git_link_list:
                                    if listOfLines[index+1].strip() != '}':
                                        wordclass = words[i + 1].strip()
                                        git_link_list.add(wordclass.replace('{', ''))
                        except BaseException:
                            print(line)

                    '''if re.search("--- a.*", line):
                        fileName = line.replace('---', '')
                        fileName = fileName.strip()
                        git_link_list.append(os.path.basename(fileName))

                    if re.search("\+\+\+ b.*", line):
                        fileName = line.replace('+++ b', 'a')
                        fileName = fileName.strip()
                        if os.path.basename(fileName) not in git_link_list:
                            git_link_list.append(os.path.basename(fileName))'''

                if len(git_link_list) > 1:
                    self.structureManager.setGitLinksToClass(git_link_list, nrOfCommits)
            except BaseException as e:
                print(e)

    def processData(self):
        for file in self.convertedFilesList:
            try:
                self.parent.printLine("Analysing " + file + " ...")
                classList = self.srcMLWrapper.getClassModel(file)
                for classStructure in classList:
                    self.structureManager.addClass(classStructure)
            except BaseException as e:
                print(e)

        self.structureManager.buildRelated()
        self.buldGitModel()
        self.structureManager.buildGit()
        self.structureManager.saveToXml()
        counter = Counter(self.structureManager)
        counter.startCount()
