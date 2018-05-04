import os
import re
import shutil

import networkx as nx

from GitWrapper import GitWrapper
from StructureManager import *
from srcMLWrapper import srcMLWrapper


class AnalysisManager:
    def __init__(self, parent, workingDir):
        self.parent = parent
        self.workingDir = workingDir
        if not os.path.isdir(self.workingDir):
            os.mkdir(self.workingDir)
        self.filesList = []
        self.convertedFilesList = []
        self.structureManager = StructureManager()
        self.srcMLWrapper = srcMLWrapper(self.workingDir)


    def setWorkingDir(self, directory):
        if os.path.isdir(directory):
            self.workingDir = directory
            try:
                os.mkdir(self.workingDir + "\~results")
            except BaseException:
                shutil.rmtree(self.workingDir + "\~results")
                os.mkdir(self.workingDir + "\~results")

            self.srcMLWrapper = srcMLWrapper(self.workingDir)
        else:
            print("Cannot set "+directory+" as working directory!")

    def getDeletedFilesXML(self):
        for root, directories, filenames in os.walk(self.workingDir+"\~deleted"):
            for filename in filenames:
                file = os.path.join(root, filename)
                returnVal, pathToFile = self.srcMLWrapper.convertFiles(file)
                self.convertedFilesList.append(pathToFile)

    def getGitCommits(self):
        gitWrapper = GitWrapper(self.workingDir)
        gitWrapper.getRepo()

        self.getDeletedFilesXML()

    def convertToXML(self):
        for file in self.filesList:
            if not re.search('\.xml', file):
                returnVal, pathToFile = self.srcMLWrapper.convertFiles(file)
                self.convertedFilesList.append(pathToFile)
                self.parent.printLine(returnVal)
            else:
                self.parent.printLine("Files already converted to XML!")
                break

    def setXMLFilesList(self, filesDir):
        for file in os.listdir(filesDir):
            self.convertedFilesList.append(filesDir+"//"+file)


    def loadStructureFromXML(self, file):
        self.structureManager.loadStructure(file)
        self.buildModel()

    def setFilesList(self, filesList):
        self.filesList = filesList

    '''    def buldGitModel(self):
        for file in os.listdir(self.workingDir+"//~diffs"):
            datafile = open(self.workingDir+"//~diffs//"+file, 'r+')
            file = file.replace('.txt', '')
            nrOfCommitsStr = file.split('FilesChanged_')[1]
            nrOfCommits = int(nrOfCommitsStr)
            git_link_list = []
            classLine = ""
            foundLineComment = False
            foundMultiLineComment = False
            foundClass = False
            try:
                for line in datafile:
                    if re.search('\'\'\'', line) and not foundMultiLineComment:
                        foundMultiLineComment = True
                    elif re.search('\'\'\'', line) and foundMultiLineComment:
                        foundMultiLineComment = False
                    elif re.search('\\\\', line):
                        foundLineComment = True
                    else:
                        foundLineComment = False

                    if foundClass and not foundMultiLineComment and not foundLineComment:
                        words = classLine.split(' ')
                        for i in range(0, len(words)):
                            word = words[i]
                            if word == 'class' and words[i+1] not in git_link_list:
                                git_link_list.append(words[i+1])
                        foundClass = False

                    if re.search('.*class .*\{', line):
                        classLine = line
                        foundClass = True
            except BaseException as e:
                print(e)

            if len(git_link_list) > 1:
                for className in git_link_list:
                    self.structureManager.setGitLinksToClass(className, git_link_list, nrOfCommits)
'''

    def buldGitModel(self):
        for file in os.listdir(self.workingDir+"//~diffs"):
            datafile = open(self.workingDir+"//~diffs//"+file, 'r+')
            file = file.replace('.txt', '')
            nrOfCommitsStr = file.split('FilesChanged_')[1]
            nrOfCommits = int(nrOfCommitsStr)
            git_link_list = []
            try:
                for line in datafile:
                    if re.search('.*::.*\{', line):
                        words = line.split(' ')
                        for i in range(0, len(words)):
                            word = words[i]
                            if re.search('.*::.*', word):
                                name = word.split('::')
                                if name not in git_link_list:
                                    git_link_list.append(name[0])

                    if re.search('.*class .*\{', line):
                        words = line.split(' ')
                        for i in range(0, len(words)):
                            word = words[i]
                            if word == 'class' and words[i + 1] not in git_link_list:
                                git_link_list.append(words[i + 1])
            except BaseException as e:
                print(e)

            if len(git_link_list) > 1:
                for className in git_link_list:
                    self.structureManager.setGitLinksToClass(className, git_link_list, nrOfCommits)

    def processData(self):
        for file in self.convertedFilesList:
            try:
                self.parent.printLine("Analysing " + file + " ...")
                classList = self.srcMLWrapper.getClassModel(file)
                for classStructure in classList:
                    #classStructure.printDetails(self.parent)
                    classStructure.buildRelated()
                    self.structureManager.addClass(classStructure)
            except BaseException as e:
                print(e)

        self.buldGitModel()
        self.structureManager.saveToXml()

    def clearNodesWithoutEdges(self, g):
        nodes = g.nodes
        nodes_to_remove = []
        for node in nodes:
            related_count = len(g.edges(node))
            if related_count == 0:
                nodes_to_remove.append(node)

        g.remove_nodes_from(nodes_to_remove)
        return g

    def drawGraph(self, g):
        size_list = []
        color_list = []
        node_list = []

        for node in g.nodes:
            node_list.append(node)
            related_count = len(g.edges(node))
            if related_count > 15:
                size_list.append(3000)
                color_list.append("#b30000")
            elif related_count > 10:
                size_list.append(2000)
                color_list.append("#cca300")
            elif related_count > 5:
                size_list.append(1000)
                color_list.append("#005580")
            else:
                size_list.append(250)
                color_list.append("#267326")

        nx.draw(g, font_size=8, width=2, with_labels=True,
                node_list=node_list,
                node_size=size_list,
                node_color=color_list)

    def createGitLinksPlot(self, plt):
        plt.figure(2)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getGitLinksTotal()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links. Count:" + str(g.number_of_edges()))
        self.drawGraph(g)

    def createGit5LinksPlot(self, plt):
        plt.figure(3)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list, b, c = classItem.getGitLinks()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links below 5. Count: " + str(g.number_of_edges()))
        self.drawGraph(g)

    def createGit20LinksPlot(self, plt):
        plt.figure(4)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                a, git_list, c = classItem.getGitLinks()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links below 20. Count:" + str(g.number_of_edges()))
        self.drawGraph(g)

    def createCodeAndGitPlot(self, plt):
        plt.figure(5)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        plt.title("Code+Git Links. Count: " + str(g.number_of_edges()))
        self.drawGraph(g)

    def createCodeLinksPlot(self, plt):
        plt.figure(1)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getRelated()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        plt.title("Code Links. Count: " + str(g.number_of_edges()))
        self.drawGraph(g)

    def buildModel(self):
        import matplotlib.pyplot as plt
        print("Number of classes: "+str(len(self.structureManager.getClassList())))
        self.createCodeLinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig1", dpi=100)
        self.createGitLinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig2", dpi=100)
        self.createGit5LinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig3", dpi=100)
        self.createGit20LinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig4", dpi=100)
        self.createCodeAndGitPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig5", dpi=100)
        plt.show()



