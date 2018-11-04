from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
import os


class TitleBar(QtWidgets.QMenuBar):
    minimizeWindow = pyqtSignal()
    maximizeWindow = pyqtSignal()
    closeWindow = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        QtWidgets.QMenuBar.__init__(self, parent)
        self.isPressed = False
        css = """
        QWidget{
            Background: #404040;
            color:white;
            font:12px bold;
            font-weight:bold;
            height: 35px;
            border-radius: 5px;
        }
        QToolButton{
            Background:#404040;
        }

        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.minimize = QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('resources/minimize.png'))

        self.maximize = QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('resources/maximize.png'))

        self.close = QtWidgets.QToolButton(self)
        self.close.setIcon(QtGui.QIcon('resources/close.png'))

        self.title = QtWidgets.QLabel(self)
        self.title.setText("  ")
        self.title.setStyleSheet("font-size: 10pt; font-family: Verdana;")

        self.user = QtWidgets.QLabel(self)
        self.user.setText(os.getlogin())
        self.user.setStyleSheet("font-size: 8pt; font-family: Verdana;")

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.close, 0, Qt.AlignTop | Qt.AlignLeft)
        hbox.addWidget(self.minimize, 0, Qt.AlignTop | Qt.AlignLeft)
        hbox.addWidget(self.maximize, 0, Qt.AlignTop | Qt.AlignLeft)
        hbox.addStretch()
        hbox.addWidget(self.title, 0, Qt.AlignTop | Qt.AlignRight)
        hbox.addStretch()
        hbox.addWidget(self.user, 0, Qt.AlignTop | Qt.AlignLeft)
        hbox.setSpacing(0)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)

        # self.connect(self.close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))
        self.close.clicked.connect(self.close_window_slot)
        self.minimize.clicked.connect(self.minimize_window_slot)
        self.maximize.clicked.connect(self.maximize_window_slot)

    def minimize_window_slot(self):
        self.minimizeWindow.emit()

    def maximize_window_slot(self):
        self.maximizeWindow.emit()

    def mousePressEvent(self, event):
        self.isPressed = True
        self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        self.isPressed = False

    def mouseMoveEvent(self, event):
        if self.isPressed:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.parent.move(x - x_w, y - y_w)

    def close_window_slot(self):
        self.closeWindow.emit()