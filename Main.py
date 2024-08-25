import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)

sys.path.append(os.path.join(os.path.dirname(__file__), 'folder_lain'))

# Import UI file
from UI.loadingScreen import Ui_loadingScreen
from UI.loginPage import Ui_loginPage
from UI.signupPage import Ui_signupPage

counter = 0
jumper = 0

class MainProgram(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_loadingScreen()
        self.ui.setupUi(self)

        self.progressBarValue(0)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Add drop shadow effect
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(15)

        self.show()

    # Progress bar value
    def progressBarValue(self, value):
        styleSheet = """
            QFrame{
                border-radius: 150px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop_1} rgba(0, 0, 0, 0), stop:{stop_2} rgba(255, 215, 0, 255));
            }
                    """
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # FIX MAX VALUE
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{stop_1}", stop_1).replace("{stop_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProg.setStyleSheet(newStylesheet)

    def progress(self):
        global counter
        global jumper
        value = counter

        htmlText = """<html><head/><body><p align="center">{VALUE}<span style=" font-size:48pt; vertical-align:sub;">%</span></p></body></html>"""

        newhtml = htmlText.replace("{VALUE}", str(int(jumper)))

        if(value > jumper):                       
            self.ui.percentage.setText(newhtml)
            jumper += 7

        if value >= 100: value = 1

        self.progressBarValue(value)
        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            self.login_page()

            # Connect the create account button to the function to show the signup page
            self.login_ui.createAcc.clicked.connect(self.show_signup_page)

        # INCREASE COUNTER
        counter += 0.5
    
    def login_page(self):
       # Replace loading screen with login page
        self.login_window = QWidget()
        self.login_ui = Ui_loginPage()
        self.login_ui.setupUi(self.login_window)

        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        self.show()

        self.setCentralWidget(self.login_window)
        self.login_window.show()


    def show_signup_page(self):
        # Replace login window with signup page
        self.signup_window = QWidget()
        self.signup_ui = Ui_signupPage()
        self.signup_ui.setupUi(self.signup_window)
        self.setCentralWidget(self.signup_window)
        self.signup_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainProgram()
    sys.exit(app.exec_())
