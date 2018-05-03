from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class GitBox(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.parent = parent
        self.line = 0
        self.setTitle("User Settings ")

        self.setStyleSheet("""font-family: Verdana;
                                  font-weight: bold;
                                  font-size: 12px;
                                  border-radius: 10px;
                                  background-color: rgba(155, 155, 144, 30);
                                  color: rgb(64, 64, 64);""")

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 18, 0, 0)
        mainLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.formWidget = QWidget()
        self.buidFormWidget()

        mainLayout.addWidget(self.formWidget)
        self.setLayout(mainLayout)

    def buidFormWidget(self):

        self.formLayout = QVBoxLayout()
        self.formLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.userField = QLineEdit()
        self.userField.setPlaceholderText("UidXXXX")
        self.userField.setFixedWidth(200)
        self.userField.setStyleSheet("border: 0.5px solid gray; border-radius: 5px;")

        self.passwordField = QLineEdit()
        self.passwordField.setPlaceholderText("Windows Password")
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.passwordField.setFixedWidth(200)
        self.passwordField.setStyleSheet("border: 0.5px solid gray; border-radius: 5px;")

        doneButton =  QPushButton("Done")
        doneButton.setStyleSheet("""QPushButton{background-color:gray; border-radius:5px;}
                                    QPushButton:hover{background-color:rgba(92, 141, 80);}""")
        doneButton.setFixedWidth(100)
        doneButton.setFixedHeight(25)
        doneButton.clicked.connect(self.registerData)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(doneButton)

        self.formLayout.addStretch()
        self.formLayout.addWidget(self.userField)
        self.formLayout.addSpacing(15)
        self.formLayout.addWidget(self.passwordField)
        self.formLayout.addSpacing(25)
        self.formLayout.addLayout(buttonLayout)
        self.formLayout.addStretch()

        self.formWidget.setFixedWidth(300)
        self.formWidget.setFixedHeight(200)
        self.formWidget.setStyleSheet("background-color: rgba(155, 155, 144, 100);")

        self.formWidget.setLayout(self.formLayout)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()

    def registerData(self):
        user = self.userField.text()
        password = self.passwordField.text()

        if user != "" and password != "":


            self.messageWidget = QWidget()
            self.messageLayout = QHBoxLayout()
            self.messageWidget.setLayout(self.messageLayout)
            self.messageWidget.hide() #box is hide until the user presses done button for the first time ,then it will be a message of succes or fail
            self.formLayout.insertWidget(1, self.messageWidget)


            self.clearLayout(self.messageLayout)
            self.messageLayout.setAlignment(QtCore.Qt.AlignCenter)

            icon = QLabel()
            message = QLabel()

            self.userField.clear()
            self.passwordField.clear()

            icon.setPixmap( QtGui.QPixmap("resources/checked-user.png"))
            message.setText("User registered!")

            self.messageLayout.addWidget(icon)
            self.messageLayout.addWidget(message)

            self.messageWidget.show()
            self.messageWidget.setStyleSheet("background-color: none;")
            
        else:

            self.messageWidget = QWidget()
            self.messageLayout = QHBoxLayout()
            self.messageWidget.setLayout(self.messageLayout)
            self.messageWidget.hide() #box is hide until the user presses done button for the first time ,then it will be a message of succes or fail
            self.formLayout.insertWidget(1, self.messageWidget)


            self.clearLayout(self.messageLayout)
            self.messageLayout.setAlignment(QtCore.Qt.AlignCenter)

            icon = QLabel()
            message = QLabel()

            self.userField.clear()
            self.passwordField.clear()

            icon.setPixmap( QtGui.QPixmap("resources/error-user.png"))
            message.setText("Please complete all fields!")


            self.messageLayout.addWidget(icon)
            self.messageLayout.addWidget(message)

            self.messageWidget.show()
            self.messageWidget.setStyleSheet("background-color: none;")


