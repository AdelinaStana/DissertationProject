import sys
from PyQt5.QtWidgets import *
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from TitleBar import TitleBar
from AnalysisManager import AnalysisManager
from CheckableDirModel import CheckableDirModel


import os


class Dialog(QMainWindow):

    def __init__(self, app, exePath=None, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.resize(900, 700)
        self.setStyleSheet("""MainWindow { border-radius: 5px; }""")

        self.app = app
        workingDir = os.path.dirname(exePath)
        self.analysisManager = AnalysisManager(self, workingDir)
        self.show()
        self.maxNormal = False

        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.titleBar = TitleBar(self)
        self.setMenuBar(self.titleBar)


        self.model = CheckableDirModel()
        self.tree = QTreeView()

        self.tree.setModel(self.model)

        self.tree.resize(640, 480)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("QTreeView { background-color: transparent; } ")

        # Creating a progress bar and setting the value limits
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)

        self.progressLine = QLabel()
        self.progressLine.setStyleSheet("QLineEdit { background-color: transparent; } ")
        # Creating a Horizontal Layout to add all the widgets
        self.boxLayout = QVBoxLayout(self)

        # Adding the widgets
        self.boxLayout.addWidget(self.tree)
        self.boxLayout.addWidget(self.progressLine)
        self.boxLayout.addWidget(self.progressBar)

        self.main_layout.addLayout(self.boxLayout)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.buildToolBar()

        self.titleBar.minimizeWindow.connect(self.minimizeWindowSlot)
        self.titleBar.maximizeWindow.connect(self.maximizeWindowSlot)
        self.titleBar.closeWindow.connect(self.closeWindowSlot)


    def buildToolBar(self):
        self.toolbar = QToolBar()
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        loadAction = QAction(QtGui.QIcon('resources/installed.png'), 'Load Files', self)
        processAction = QAction(QtGui.QIcon('resources/run.png'), 'Process Files', self)
        xmlLoadAction = QAction(QtGui.QIcon('resources/load.png'), 'XML File', self)

        processAction.triggered.connect(self.processFilesClicked)
        xmlLoadAction.triggered.connect(self.loadXmlClicked)
        loadAction.triggered.connect(self.loadFilesClicked)

        self.toolbar.addAction(loadAction)
        self.toolbar.addAction(processAction)
        self.toolbar.addAction(xmlLoadAction)

        self.toolbar.setIconSize(QtCore.QSize(65, 65))

        self.toolbar.setFocus()

        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon | QtCore.Qt.LeftToolBarArea)

        self.toolbar.setStyleSheet("""QToolBar {
                     background-color: rgba(155, 155, 144, 100); }""")

        for action in self.toolbar.actions():
            widget = self.toolbar.widgetForAction(action)
            widget.setFixedSize(70, 70)


    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def paintEvent(self, event):
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background,
                         QtGui.QBrush(QtGui.QPixmap("resources/theme.png").scaled(self.size())))
        self.setPalette(palette)

    @QtCore.pyqtSlot()
    def closeWindowSlot(self):
        self.deleteLater()

    @QtCore.pyqtSlot()
    def minimizeWindowSlot(self):
        self.showMinimized()

    @QtCore.pyqtSlot()
    def maximizeWindowSlot(self):
        if self.maxNormal:
            self.resize(800, 600)
            self.maxNormal = False
            self.titleBar.maximize.setIcon(QtGui.QIcon('resources/maximize.png'))
            frameGm = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())

        else:
            screen = QDesktopWidget().screenGeometry()
            self.setGeometry(0, 0, screen.width(), screen.height() - 30)
            self.maxNormal = True
            self.titleBar.maximize.setIcon(QtGui.QIcon('resources/unmaximize.png'))

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def settingsClicked(self):
        self.clearLayout(self.main_layout)

    '''def loadXmlClicked1(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select XML File"))

        filesList = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
        self.analysisManager.setXMLFilesList(filesList)
        total = len(filesList)
        count = 1
        for file in filesList:
            self.printLine(file + "\n")
            self.progressBar.setValue((count * 100) / total)
            self.progressBar.update()
            count += 1'''

    def loadXmlClicked(self):
        xmlFile = str(QFileDialog.getOpenFileName(self, "Select XML File")[0])

        self.progressBar.setValue(0)
        self.printLine("Loading data from XML structure. Please wait ...\n")
        self.progressBar.update()
        self.analysisManager.loadStructureFromXML(xmlFile)
        self.progressBar.setValue(100)
        self.progressBar.update()

    def loadFilesClicked(self):
        filenames = self.model.exportChecked()
        repoDir = self.model.rootDir
        self.analysisManager.setFilesList(filenames)
        self.analysisManager.setWorkingDir(repoDir)
        self.printLine("Files loaded:\n")
        total = len(filenames)
        count = 1
        for file in filenames:
            self.printLine(file+"\n")
            self.progressBar.setValue((count*100)/total)
            self.progressBar.update()
            count += 1

        self.printLine("Total number of files loaded : {}".format(total))

    def processFilesClicked(self):
        self.analysisManager.setXMLFilesList(self.model.rootDir+"/~Temp/")
        self.printLine("Converting to XML .......")
        self.analysisManager.convertToXML()
        self.printLine("Getting commits .......")
        self.analysisManager.getGitCommits()
        self.printLine("Building model .......")
        self.analysisManager.processData()
        self.analysisManager.buildModel()

    def printLine(self, text):
        self.app.processEvents()
        self.progressLine.setText(text)

    def changeLayout(self):
        self.clearLayout(self.main_layout)

        self.main_widget.setLayout(self.main_layout)
        self.toolbar.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    ex = Dialog(app, sys.argv[0])
    ex.resize(600, 400)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
