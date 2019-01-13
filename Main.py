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
        self.analysisManager = None
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

        self.build_tool_bar()

        self.titleBar.minimizeWindow.connect(self.minimize_window_slot)
        self.titleBar.maximizeWindow.connect(self.maximize_window_slot)
        self.titleBar.closeWindow.connect(self.close_window_slot)

    def build_tool_bar(self):
        self.toolbar = QToolBar()
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        load_action = QAction(QtGui.QIcon('resources/installed.png'), 'Load Files', self)
        process_action = QAction(QtGui.QIcon('resources/run.png'), 'Process Files', self)
        xml_load_action = QAction(QtGui.QIcon('resources/load.png'), 'XML File', self)

        process_action.triggered.connect(self.process_files_clicked)
        xml_load_action.triggered.connect(self.load_xml_clicked)
        load_action.triggered.connect(self.load_files_clicked)

        self.toolbar.addAction(load_action)
        self.toolbar.addAction(process_action)
        self.toolbar.addAction(xml_load_action)

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
    def close_window_slot(self):
        self.deleteLater()

    @QtCore.pyqtSlot()
    def minimize_window_slot(self):
        self.showMinimized()

    @QtCore.pyqtSlot()
    def maximize_window_slot(self):
        if self.maxNormal:
            self.resize(800, 600)
            self.maxNormal = False
            self.titleBar.maximize.setIcon(QtGui.QIcon('resources/maximize.png'))
            frame_gm = self.frameGeometry()
            center_point = QDesktopWidget().availableGeometry().center()
            frame_gm.moveCenter(center_point)
            self.move(frame_gm.topLeft())

        else:
            screen = QDesktopWidget().screenGeometry()
            self.setGeometry(0, 0, screen.width(), screen.height() - 30)
            self.maxNormal = True
            self.titleBar.maximize.setIcon(QtGui.QIcon('resources/unmaximize.png'))

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def settings_clicked(self):
        self.clear_layout(self.main_layout)

    def load_xml_clicked(self):
        xml_file = str(QFileDialog.getOpenFileName(self, "Select XML File")[0])

        self.progressBar.setValue(0)
        self.print_line("Loading data from XML structure. Please wait ...\n")
        self.progressBar.update()
        xml_dir = os.path.dirname(xml_file)
        self.analysisManager = AnalysisManager(self, xml_dir)
        self.analysisManager.load_structure_from_xml(xml_file)
        self.progressBar.setValue(100)
        self.progressBar.update()

    def load_files_clicked(self):
        file_names = self.model.export_checked()
        repo_dir = self.model.rootDir
        self.analysisManager = AnalysisManager(self, repo_dir)
        self.analysisManager.set_files_list(file_names)
        self.print_line("Files loaded:\n")
        total = len(file_names)
        count = 1
        self.progressBar.setValue(0)
        self.progressBar.update()
        for file in file_names:
            self.print_line(file + "\n")
            self.progressBar.setValue((count*100)/total)
            self.progressBar.update()
            count += 1

        self.print_line("Total number of files loaded : {}".format(total))

    def process_files_clicked(self):
        self.get_res()
        # self.print_line("Converting to XML .......")
        # self.analysisManager.convert_to_xml()
        # self.analysisManager.set_xml_files_list(self.model.rootDir + "/~Temp/")
        # self.print_line("Getting commits .......")
        # self.analysisManager.get_git_commits()
        # self.print_line("Processing data .......")
        # self.analysisManager.process_data()

    def print_line(self, text):
        self.app.processEvents()
        self.progressLine.setText(text)

    def change_layout(self):
        self.clear_layout(self.main_layout)

        self.main_widget.setLayout(self.main_layout)
        self.toolbar.setEnabled(True)

    def get_git_diff_struct(self):
        accepted_suffix = ['cpp', 'h', 'cc', 'c++', 'java', 'cs']
        repo_list = []
        for repo in repo_list:
            print(repo)
            file_names = []
            for path, dirs, files in os.walk(repo):
                for filename in files:
                    if QtCore.QFileInfo(filename).suffix() in accepted_suffix:
                                file_names.append(os.path.join(path, filename))
            print(len(file_names))
            self.analysisManager = AnalysisManager(self, repo)
            self.analysisManager.set_files_list(file_names)
            self.analysisManager.convert_to_xml()
            self.analysisManager.set_xml_files_list(repo + "/~Temp/")
            self.analysisManager.get_git_commits()

    def get_res(self):
        accepted_suffix = ['cpp', 'h', 'cc', 'c++', 'java', 'cs']
        repo_list = [
                    "E:\\faculta\\Master\\TestProjects\\mcidasv",
                    "E:\\faculta\\Master\\TestProjects\\antlr4",
                    "E:\\faculta\\Master\\TestProjects\\robolectric",
                    "E:\\faculta\\Master\\TestProjects\\PowerShell",
                    "E:\\faculta\\Master\\TestProjects\\WeiXinMPSDK",
                    "E:\\faculta\\Master\\TestProjects\\ArchiSteamFarm",
                    "E:\\faculta\\Master\\TestProjects\\VisualStudio",
                    "E:\\faculta\\Master\\TestProjects\\CppSharp",
                    "E:\\faculta\Master\\TestProjects\\bluecove",
                    "E:\\faculta\Master\\TestProjects\\shipkit",
                    "E:\\faculta\Master\\TestProjects\\ShareX",
                    "E:\\faculta\Master\\TestProjects\\RxJava",
                    "E:\\faculta\Master\\TestProjects\\restfb",
                    "E:\\faculta\Master\\TestProjects\\powermock",
                    "E:\\faculta\Master\\TestProjects\\orleans",
                    "E:\\faculta\Master\\TestProjects\\OpenClinica",
                    "E:\\faculta\Master\\TestProjects\\mockito",
                    "E:\\faculta\Master\\TestProjects\\jellyfin",
                    "E:\\faculta\Master\\TestProjects\\grizzly",
                    "E:\\faculta\Master\\TestProjects\\cli",
                    "E:\\faculta\Master\\TestProjects\\aeron",
                    "E:\\faculta\Master\\TestProjects\\Avalonia",
                    "E:\\faculta\Master\\TestProjects\\aspnetboilerplate",
                    "E:\\faculta\Master\\TestProjects\\EntityFrameworkCore",
                    "E:\\faculta\Master\\TestProjects\\cake",
                    "E:\\faculta\Master\\TestProjects\\aima-java",
                    "E:\\faculta\Master\\TestProjects\\metro-jax-ws"
                     ]
        for repo in repo_list:
            print("______________________________________________________________________________________")
            print(repo)
            file_names = []
            for path, dirs, files in os.walk(repo):
                for filename in files:
                    if QtCore.QFileInfo(filename).suffix() in accepted_suffix:
                                file_names.append(os.path.join(path, filename))
            self.analysisManager = AnalysisManager(self, repo)
            self.analysisManager.set_files_list(file_names)
            self.analysisManager.set_xml_files_list(repo + "/~Temp/")
            self.analysisManager.process_data()


def main():
    app = QApplication(sys.argv)
    ex = Dialog(app, sys.argv[0])
    ex.resize(600, 400)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    noGui = False
    # tbd
    for arg in sys.argv:
        if "-noGui=" in arg:
            noGui = True
        if "-folderPath" in arg:
            folderPath = arg
        if "-xmlPath" in arg:
            xmlPath = arg

    if not noGui:
        main()