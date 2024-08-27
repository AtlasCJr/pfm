import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)

from UI.mainMenu import Ui_MainWindow

class MainProgram(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        # If menu bar button pressed, change the stacked widget to the corresponding page
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))   
        self.ui.loginButton.clicked.connect(self.show_loginsignup)
        self.ui.loginButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.loginsignup))
        self.ui.inputdataButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.inputData)) 
        self.ui.showdatabutton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.showData))   
        self.ui.chatbotButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.chatBot))
        self.ui.profileButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.profile))
        self.ui.aboutButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.about))

        # Connecting buttons within the loginsignup widget to the innerStackedWidget innerStackedWidget
        self.ui.createAcc.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.signupPage))
        self.ui.forgotPW.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.changePW))
        self.ui.backtoLogin.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage))
        self.ui.backtoLogin_2.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage))

    def show_loginsignup(self):
    # Show the loginsignup widget and set innerStackedWidget to loginPage
        self.ui.stackedWidget.setCurrentWidget(self.ui.loginsignup)
        self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainProgram()
    window.show()
    sys.exit(app.exec_())