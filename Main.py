import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from UI.Master import Ui_Master
from UI.loadingScreen import Ui_loadingScreen

from Functions.edit_database import isUsernameAvailable, addAccount, checkAccount, getAccount
from Functions.variables import Account

class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_loadingScreen()
        self.ui.setupUi(self)

        self.progressBarValue(0)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(15)

        self.show()

    def progressBarValue(self, value):
        styleSheet = """
            QFrame{
                border-radius: 150px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop_1} rgba(0, 0, 0, 0), stop:{stop_2} rgba(255, 215, 0, 255));
            }
        """
        progress = (100 - value) / 100.0
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        newStylesheet = styleSheet.replace("{stop_1}", stop_1).replace("{stop_2}", stop_2)
        self.ui.circularProg.setStyleSheet(newStylesheet)

    def progress(self):
        global counter
        global jumper
        value = counter

        htmlText = """<html><head/><body><p align="center">{VALUE}<span style=" font-size:48pt; vertical-align:sub;">%</span></p></body></html>"""

        newhtml = htmlText.replace("{VALUE}", str(int(jumper)))

        if value > jumper:                       
            self.ui.percentage.setText(newhtml)
            jumper += 7

        if value >= 100:
            value = 1

        self.progressBarValue(value)

        if counter > 100:
            self.timer.stop()
            self.close()  # Close the loading screen
            self.setMaster()  # Show the main program window

        counter += 0.5

    def setMaster(self):
        self.main_window = MainProgram()
        self.main_window.show()

class MainProgram(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_Master()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Header Buttons
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.loginButton.clicked.connect(self.Authentication)
        self.ui.inputdataButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.inputData)) 
        self.ui.showdatabutton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.showData))   
        self.ui.chatbotButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.chatBot))
        self.ui.profileButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.profile))
        self.ui.aboutButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.about))

        # Authentication Buttons
        self.ui.LI_buttonForgetPassword.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.changePW))  # Login -> CP
        self.ui.SI_buttonLogIn.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage))          # SignIn -> Login
        self.ui.LI_buttonSignIn.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.signupPage))        # Login -> SignIn
        self.ui.CP_buttonLogIn.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage))          # CP -> Login

        self.ui.SI_buttonSI.clicked.connect(self.handleSignIn)
        self.ui.LI_buttonLI.clicked.connect(self.handleLogIn)

    def Authentication(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loginsignup)
        self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage)

    def handleSignIn(self):
        username = self.ui.SI_inputUsername.text()

        if username == "":
            self.ui.SI_ErrorMsg.setText("Username cannot be empty.")
            return
        if len(username) <= 5:
            self.ui.SI_ErrorMsg.setText("Username cannot be less than 5 characters.")
            return
        if isUsernameAvailable(username):
            self.ui.SI_ErrorMsg.setText("Username has already been taken.")
            return
        
        password1 = self.ui.SI_inputPassword1.text()
        password2 = self.ui.SI_inputPassword2.text()

        if password1 == "" or password2 == "":
            self.ui.SI_ErrorMsg.setText("Password cannot be empty.")
            return
        if len(password1) <= 5:
            self.ui.SI_ErrorMsg.setText("Password cannot be less than 5 characters.")
            return
        if password1 != password2:
            self.ui.SI_ErrorMsg.setText("The typed password doesn't match.")
            return

        security_q = int(self.ui.SI_dropdownSecurity.currentText()[1])
        security_a = self.ui.SI_inputSecurity.text()

        if security_a == "":
            self.ui.SI_ErrorMsg.setText("Security answer cannot be empty.")
            return

        tos = self.ui.SI_checkboxTerm.isChecked()

        if not tos:
            self.ui.SI_ErrorMsg.setText("Terms of Service has to be checked.")
            return
        
        newAcc = Account(username, password1, security_q, security_a)
        self.ui.SI_ErrorMsg.setText("")
        addAccount(newAcc)

    def handleLogIn(self) -> Account:
        username = self.ui.LI_inputUsername.text()
        password = self.ui.LI_inputPassword.text()

        isCorrect = checkAccount(username, password)

        print(isCorrect)

        if isCorrect:
            self.ui.LI_ErrorMsg.text("")
            return getAccount(username)
        else:
            self.ui.LI_ErrorMsg.text("Wrong username or password.")
            return None




if __name__ == "__main__":

    os.system("cls" if os.name == "nt" else "clear")

    global counter, jumper
    counter = 0
    jumper = 0

    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    sys.exit(app.exec_())