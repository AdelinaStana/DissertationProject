from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import os


class CheckableDirModel(QDirModel):
    def __init__(self, parent=None):
        QDirModel.__init__(self, None)
        self.checks = {}
        self.rootDir = None

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return self.checkState(index)
        return QDirModel.data(self, index, role)

    def flags(self, index):
        return QDirModel.flags(self, index) | QtCore.Qt.ItemIsUserCheckable

    def checkState(self, index):
        while index.isValid():
            if index in self.checks:
                return self.checks[index]
            index = index.parent()
        return QtCore.Qt.Unchecked

    def are_parent_and_child(self,parent, child):
        while child.isValid():
            if child == parent:
                return True
            child = child.parent()
        return False

    def setData(self, index, value, role):
        checksList = []
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            try:
                self.layoutAboutToBeChanged.emit()
                # for i, v in self.checks.items():
                #     if self.are_parent_and_child(index, i):
                #         checksList.append(i)
                # for index in checksList:
                #     self.checks.pop(index)
                self.checks[index] = value
                self.layoutChanged.emit()
            except BaseException as e:
                print(e)
            return True

        return QDirModel.setData(self, index, value, role)

    def exportChecked(self, acceptedSuffix=['cpp', 'h', 'cc','c++','java','cs']):
        selection=  set()
        for index in self.checks.keys():
            if self.checks[index] == QtCore.Qt.Checked:
                for path, dirs, files in os.walk(self.filePath(index)):
                    if self.rootDir is None:
                        self.rootDir = path
                    for filename in files:
                        if QtCore.QFileInfo(filename).completeSuffix() in acceptedSuffix:
                            if self.checkState(self.index(os.path.join(path, filename))) == QtCore.Qt.Checked:
                                try:
                                    selection.add(os.path.join(path, filename))
                                except:
                                    pass
        return selection
