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
        self.structureManager = StructureManager(self.workingDir)
        self.srcMLWrapper = srcMLWrapper(self.workingDir)
        self.resultsText = ""

    def setWorkingDir(self, directory):
        if os.path.isdir(directory):
            self.workingDir = directory
            try:
                os.mkdir(self.workingDir + "\~results")
            except BaseException:
                shutil.rmtree(self.workingDir + "\~results")
                os.mkdir(self.workingDir + "\~results")

            self.srcMLWrapper = srcMLWrapper(self.workingDir)
            self.structureManager = StructureManager(self.workingDir)
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

        #self.getDeletedFilesXML()

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

    def setXMLFilesList(self, filesDir):
        self.convertedFilesList = []
        for r, d, f in os.walk(filesDir):
            for file in f:
                self.convertedFilesList.append(os.path.join(r, file))


    def loadStructureFromXML(self, file):
        self.structureManager.loadStructure(file)
        self.buildModel()

    def setFilesList(self, filesList):
        self.filesList = filesList

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
                datafile = open(self.workingDir+"//~diffs//"+file, 'r+', encoding="utf8", errors='ignore').read()
                #datafile = self.removeComments(datafile)
                datafile = self.removeGitSimbols(datafile)
                file = file.replace('.txt', '')
                nrOfCommitsStr = file.split('FilesChanged_')[1]
                nrOfCommits = int(nrOfCommitsStr)
                git_link_list = []
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
                                        git_link_list.append(wordclass.replace('{', ''))
                        except BaseException:
                            print(line)

                    '''if re.search("--- a.*", line):
                        fileName = line.replace('---', '')
                        fileName = fileName.strip()
                        git_link_list.append(fileName)

                    if re.search("\+\+\+ b.*", line):
                        fileName = line.replace('+++ b', 'a')
                        fileName = fileName.strip()
                        if fileName not in git_link_list:
                            git_link_list.append(fileName)'''

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
                    #classStructure.printDetails(self.parent)
                    self.structureManager.addClass(classStructure)
            except BaseException as e:
                print(e)

        self.structureManager.buildRelated()
        self.buldGitModel()
        self.structureManager.buildGit()
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

    def createCodeLinksPlot(self, plt):
        print(".")
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
        print("Number of classes: " + str(g.number_of_nodes())+",")
        plt.title("Code Links. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_nodes()) + ","
        self.resultsText += str(g.number_of_edges())+","
        #self.drawGraph(g)

    def createGit5LinksPlot(self, plt):
        print(".")
        plt.figure(2)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getGit5Links()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links below 5. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        #######################################################################3
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow5(2)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        g = self.clearNodesWithoutEdges(g)
        self.resultsText += str(g.number_of_edges()) + ","

        #######################################################################3
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow5(3)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #######################################################################3
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow5(4)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        g = self.clearNodesWithoutEdges(g)
        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def createGit10LinksPlot(self, plt):
        print(".")
        plt.figure(3)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getGit10Links()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links below 20. Count:" + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","
        #########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow10(2)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        #########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow10(3)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow10(4)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def createGit20LinksPlot(self, plt):
        print(".")
        plt.figure(4)
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getGit20Links()
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        g = self.clearNodesWithoutEdges(g)
        plt.title("Git Links above 20. Count:" + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        #############################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow20(2)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        #############################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow20(3)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        #############################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurencesBelow20(4)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def createGitTotalLinksPlot(self, plt):
        print(".")
        plt.figure(5)
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
        self.resultsText += str(g.number_of_edges())+","
        ###########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurrencesTotal(2)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        ###########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurrencesTotal(3)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        ###########################################################################
        g = nx.Graph()

        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                git_list = classItem.getOccurrencesTotal(4)
                for related in git_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","


        #self.drawGraph(g)

    def createCodeAndTotalGitPlot(self, plt):
        print(".")
        plt.figure(6)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatchTotal()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        plt.title("Code+Git Links Total. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        ################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatchOccTotal(2)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        ################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatchOccTotal(3)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        ################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatchOccTotal(4)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def createCodeAndGitPlot5(self, plt):
        print(".")
        plt.figure(7)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch5()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        plt.title("Code+Git Links < 5. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        ######################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch5Occ(2)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        g = self.clearNodesWithoutEdges(g)
        self.resultsText += str(g.number_of_edges())+","

        ######################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch5Occ(3)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        g = self.clearNodesWithoutEdges(g)
        self.resultsText += str(g.number_of_edges()) + ","

        ######################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch5Occ(4)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        g = self.clearNodesWithoutEdges(g)
        self.resultsText += str(g.number_of_edges()) + ","


        #self.drawGraph(g)

    def createCodeAndGitPlot10(self, plt):
        print(".")
        plt.figure(8)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch10()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        plt.title("Code+Git Links <= 10. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        ###################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch10Occ(2)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        self.resultsText += str(g.number_of_edges())+","

        ###################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch10Occ(3)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        self.resultsText += str(g.number_of_edges())+","

        ###################################################################

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch10Occ(4)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def createCodeAndGitPlot20(self, plt):
        print(".")
        plt.figure(9)
        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch20()
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)
        self.clearNodesWithoutEdges(g)

        plt.title("Code+Git Links <= 20. Count: " + str(g.number_of_edges()))
        self.resultsText += str(g.number_of_edges())+","

        #############################################################3

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch20Occ(2)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        #############################################################3

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch20Occ(3)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges())+","

        #############################################################3

        g = nx.Graph()
        try:
            for classItem in self.structureManager.getClassList():
                g.add_node(classItem.name)
                related_list = classItem.getMatch20Occ(4)
                for related in related_list:
                    g.add_edge(classItem.name, related)
        except BaseException as e:
            print(e)

        self.resultsText += str(g.number_of_edges()) + ","

        #self.drawGraph(g)

    def buildModel(self):
        import matplotlib.pyplot as plt
        try:
            self.createCodeLinksPlot(plt)
            self.createGit5LinksPlot(plt)
            self.createGit10LinksPlot(plt)
            self.createGit20LinksPlot(plt)
            self.createGitTotalLinksPlot(plt)
            self.createCodeAndGitPlot5(plt)
            self.createCodeAndGitPlot10(plt)
            self.createCodeAndGitPlot20(plt)
            self.createCodeAndTotalGitPlot(plt)

            print(self.resultsText)
        except BaseException as e:
            print(e)

'''
def buildModel(self):
    import matplotlib.pyplot as plt
    try:
        self.createCodeLinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig1", dpi=100)
        self.createGit5LinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig2", dpi=100)
        self.createGit10LinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig3", dpi=100)
        self.createGit20PlusLinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig4", dpi=100)
        self.createGitTotalLinksPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig5", dpi=100)
        self.createCodeAndGitPlot(plt)
        plt.savefig(self.workingDir + "\~results\\fig6", dpi=100)
        self.createCodeAndGitPlot5(plt)
        plt.savefig(self.workingDir + "\~results\\fig7", dpi=100)
        self.createCodeAndGitPlot20(plt)
        plt.savefig(self.workingDir + "\~results\\fig8", dpi=100)
        self.createCodeAndGitPlot20Plus(plt)
        plt.savefig(self.workingDir + "\~results\\fig9", dpi=100)
        plt.show()

        print(self.resultsText)
    except BaseException as e:
        print(e)'''

