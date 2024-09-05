import sys
import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import *

from UI.Master import Ui_Master
from UI.loadingScreen import Ui_loadingScreen
from UI.Alert import Ui_Alert

from Functions.database import *
from Functions.classes import Account, botWorker
from Functions.data_analysis import *
from Functions.others import *


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

class Alert(QDialog):
    def __init__(self, text: str):
        QDialog.__init__(self)

        self.ui = Ui_Alert()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.msg.setText(text)

        self.result = False

        self.ui.CANCEL.clicked.connect(self.CANCEL)
        self.ui.YES.clicked.connect(self.CONTINUE)

    def CANCEL(self):
        self.result = False
        self.close()

    def CONTINUE(self):
        self.result = True
        self.close()

    def getResult(self):
        self.exec_()
        return self.result

class MainProgram(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        global start
        start = datetime.now()

        self.ui = Ui_Master()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.currentAcc = None
        self.selectedTransactionID = None

        try: self.currentAcc = getLastUser()
        except Exception: pass

        self.accountChanged()

        self.graphIndex = [0]

        # Header Buttons
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.loginButton.clicked.connect(self.Authentication)
        self.ui.inputdataButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.inputData))
        self.ui.visualizeButton.clicked.connect(lambda: (self.setupVisualize(), self.ui.stackedWidget.setCurrentWidget(self.ui.visualize)))
        self.ui.analyzeButton.clicked.connect(lambda: (self.setupAnalyze(), self.ui.stackedWidget.setCurrentWidget(self.ui.analyze)))
        self.ui.chatbotButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.chatBot))
        self.ui.aboutButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.about))
        self.ui.profileButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.profile))
        self.ui.editButton.clicked.connect(lambda: (self.searchData(), self.ui.stackedWidget.setCurrentWidget(self.ui.edit)))

        # Authentication
        self.ui.LI_buttonForgetPassword.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.forgetPW))  # Login -> FP
        self.ui.LI_buttonSignIn.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.signupPage))        # Login -> SignIn
        self.ui.SI_buttonLogIn.clicked.connect(lambda: self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage))          # SignIn -> Login
        self.ui.FP_buttonSavePW.clicked.connect(lambda: self.handleForgetPW)                                                                                                                      # FP -> Login
        self.ui.CP_buttonSavePW.clicked.connect(lambda: self.ui.setCurrentWidget(self.ui.profile))                              # CP -> Profile


        self.ui.SI_buttonSI.clicked.connect(self.handleSignIn)                                                                  # Sign In
        self.ui.LI_buttonLI.clicked.connect(self.handleLogIn)                                                                   # Log In
        self.ui.CP_buttonSavePW.clicked.connect(self.handleChangePW)                                                            # Change Password

        self.ui.LI_inputUsername.returnPressed.connect(lambda: self.ui.LI_inputPassword.setFocus())
        self.ui.LI_inputPassword.returnPressed.connect(self.handleLogIn)

        self.ui.CP_inputSecAnswer.returnPressed.connect(lambda: self.ui.CP_inputPassword1.setFocus())
        self.ui.CP_inputPassword1.returnPressed.connect(lambda: self.ui.CP_inputPassword2.setFocus())
        self.ui.CP_inputPassword2.returnPressed.connect(self.handleChangePW)

        self.ui.FP_inputUsername.returnPressed.connect(lambda: self.ui.FP_inputSecAnswer.setFocus())
        self.ui.FP_inputSecAnswer.returnPressed.connect(lambda: self.ui.FP_inputPassword1.setFocus())
        self.ui.FP_inputPassword1.returnPressed.connect(lambda: self.ui.FP_inputPassword2.setFocus())
        self.ui.FP_inputPassword2.returnPressed.connect(lambda: self.ui.FP_buttonSavePW.click())

        # Visualize

        # Edit
        self.ui.calendarWidget.selectionChanged.connect(self.searchData)
        self.ui.ED_updateButton.clicked.connect(self.handleUpdateTransaction)
        self.ui.ED_deleteButton.clicked.connect(self.handleDeleteTransaction)

        # Analysis
        self.ui.AN_backButton.clicked.connect(self.handleBackButton)
        self.ui.AN_forwardButton.clicked.connect(self.handleForwardButton)

        # Chatting
        self.ui.userChatInput.returnPressed.connect(self.askGemini)

        # Profile
        self.ui.PF_changePassword.clicked.connect(lambda: (
            self.ui.stackedWidget.setCurrentWidget(self.ui.loginsignup),
            self.ui.innerstackedWidget.setCurrentWidget(self.ui.changePW)
        ))
        self.ui.PF_logOut.clicked.connect(self.handleLogOut)
        self.ui.PF_deleteAccount.clicked.connect(self.handleDeleteAcc)

        # Upload
        self.ui.ID_addTransaction.clicked.connect(self.handleAddTransaction)

    def handleAddTransaction(self):
        item = self.ui.ID_inputTransaction.text()
        type = self.ui.ID_dropdownType.currentIndex()
        date = self.ui.ID_calendarWidget.selectedDate().toPyDate()
        # date = date.toString("yyyy-MM-dd")
        value = self.ui.ID_inputValue.text()

        time = self.ui.ID_timeEdit.time().toPyTime()

        if item == "":
            self.ui.ID_errorMsg.setText("Item name cannot be empty.")
            return
        
        if value == "":
            self.ui.ID_errorMsg.setText("Value cannot be empty.")
            return
        try: int(value)
        except Exception:
            self.ui.ID_errorMsg.setText("Value cannot be converted to int. Please input numbers only.")
            return
        if int(value) < 0:
            self.ui.ID_errorMsg.setText("Value cannot be negative.")
            return
        
        if date > datetime.now().date():
            self.ui.ID_errorMsg.setText("Date cannot be later than today.")
            return
        
        category = 0 if type < 10 else 1
        value = int(value)
        date = date.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M:%S")

        self.ui.ID_errorMsg.clear()
        addTransaction(self.currentAcc, item, type, category, value, date)

        self.ui.ID_inputTransaction.clear()
        self.ui.ID_dropdownType.clear()
        self.ui.ID_inputValue.clear()

        self.currentAcc = getAccount(self.currentAcc.username)
        self.accountChanged()

    def handleDeleteTransaction(self):
        alert = Alert("You are about to delete your chosen transaction.")
        answer = alert.getResult()

        if answer:
            deleteTransaction(self.currentAcc, self.selectedTransactionID)

            self.ui.ED_Item.clear()
            self.ui.ED_Type.setCurrentIndex(0)
            self.ui.ED_Value.clear()

            self.currentAcc = getAccount(self.currentAcc.username)
            self.accountChanged()
            self.searchData()
        else:
            return

    def handleUpdateTransaction(self):
        alert = Alert("You are about to change your chosen transaction.")
        answer = alert.getResult()

        if answer:
            item = self.ui.ED_Item.text()
            type = self.ui.ED_Type.currentIndex()
            category = 0 if type < 10 else 1
            value = self.ui.ED_Value.text()
            date = self.ui.ED_Date.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")

            editTransaction(self.currentAcc, self.selectedTransactionID, item, type, category, value, date)

            print("changed")

            self.ui.ED_Item.clear()
            self.ui.ED_Type.setCurrentIndex(0)
            self.ui.ED_Value.clear()

            self.accountChanged()
            self.searchData()
        else:
            return

    def handleDeleteAcc(self):
        alert = Alert("You are about to delete your account.")
        answer = alert.getResult()

        if answer:
            updateLastUser("")
            deleteAccount(self.currentAcc)
            self.currentAcc = None
            self.accountChanged()
        else:
            return

    def handleLogOut(self):
        alert = Alert("You are about to log out.")
        answer = alert.getResult()

        if answer:
            updateLastUser("")
            self.currentAcc = None
            self.accountChanged()
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        else:
            return

    def setupVisualize(self):
        self.ED.plotAll("YEAR", "YEAR", (0), self.ui.VI_Graph1)
        self.ui.VI_Graph1.update()

        self.ED.plotCategory(0, self.ui.VI_Graph2)
        self.ui.VI_Graph2.update()

        self.graphAnalyze(self.graphIndex[0])

    def graphAnalyze(self, index:int):
        self.ED.plotTimeCycle(index, self.ui.VI_Graph3)
        self.ui.VI_Graph3.update()

    def handleForwardButton(self):
        self.graphIndex[0] -= 1
        self.graphIndex[0] %= 5
        self.graphAnalyze(self.graphIndex[0])

    def handleBackButton(self):
        self.graphIndex[0] -= 1
        self.graphIndex[0] %= 5
        self.graphAnalyze(self.graphIndex[0])

    def setupAnalyze(self):
        self.ui.linregTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.linregTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        linreg = self.ED.getLinReg()
        for j, y in enumerate(linreg):
            for i, x in enumerate(y):
                item = QTableWidgetItem(formatNumber(x))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.linregTable.setItem(j, i, item)
        
        question = f"""
        This is my current economical state. I live in Indonesia. Please tell me about my current status.
        Expenses:
        Daily: {linreg[0][0]}
        Weekly: {linreg[0][1]}
        Monthly: {linreg[0][2]}
        Quarterly: {linreg[0][3]}
        Annually: {linreg[0][4]}

        Revenue:
        Daily: {linreg[1][0]}
        Weekly: {linreg[1][1]}
        Monthly: {linreg[1][2]}
        Quarterly: {linreg[1][3]}
        Annually: {linreg[1][4]}
        """

        self.botWorker = botWorker(question)
        self.botWorker.resultReady.connect(self.analyzeTable)
        self.botWorker.start()

    def analyzeTable(self, answer):
        self.ui.AN_Explanation.setText(answer)

    def searchData(self):
        date = self.ui.calendarWidget.selectedDate()
        date = date.toString("yyyy-MM-dd")

        self.selectedData = self.old_data[self.old_data['CREATED_AT'].str.startswith(date)]

        while self.ui.verticalLayout_18.count():
            item = self.ui.verticalLayout_18.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for _, row in self.selectedData.iterrows():
            self.addDataFrame(row['ITEM'], row['VALUE'], row['TRANSACTION_ID'])
    
    def showData(self, id:str):
        row = self.selectedData[self.selectedData['TRANSACTION_ID'] == id]

        self.selectedTransactionID = id

        self.ui.ED_Item.setText(str(row['ITEM'].values[0]))
        self.ui.ED_Value.setText(str(row['VALUE'].values[0]))
        self.ui.ED_Type.setCurrentIndex(int(row['TYPE'].values[0]))
        self.ui.ED_Date.setDateTime(QDateTime.fromString(str(row['CREATED_AT'].values[0]), "yyyy-MM-dd HH:mm:ss"))

    def addDataFrame(self, title:str, price:int, id:str):
        FRAME = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FRAME.sizePolicy().hasHeightForWidth())
        FRAME.setSizePolicy(sizePolicy)
        FRAME.setMinimumSize(QtCore.QSize(0, 75))
        FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        FRAME.setFrameShadow(QtWidgets.QFrame.Raised)


        LABEL = QtWidgets.QLabel(FRAME)
        LABEL.setStyleSheet("color: rgb(255, 255, 255);")
        LABEL.setText(f"""
        <html><head/><body>
            <p><span style=\" font-weight:600;\">
                {title}
            </span></p>
            <p>
                {str(price)}
            </p>
        </body></html>
        """)

        LAYOUT = QtWidgets.QVBoxLayout(FRAME)
        LAYOUT.addWidget(LABEL)

        FRAME.mousePressEvent = lambda event, trans_id=id: self.showData(trans_id)

        self.ui.verticalLayout_18.addWidget(FRAME)

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
        if " " in username:
            self.ui.SI_ErrorMsg.setText("Username cannot has spaces.")
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
        if " " in password1:
            self.ui.SI_ErrorMsg.setText("Password cannot has spaces.")
            return
        if password1 != password2:
            self.ui.SI_ErrorMsg.setText("The typed password doesn't match.")
            return

        security_q = int(self.ui.SI_dropdownSecurity.currentText()[3])
        security_a = self.ui.SI_inputSecurity.text()

        if security_a == "":
            self.ui.SI_ErrorMsg.setText("Security answer cannot be empty.")
            return

        tos = self.ui.SI_checkboxTerm.isChecked()
        security_a = security_a.lower()

        if not tos:
            self.ui.SI_ErrorMsg.setText("Terms of Service has to be checked.")
            return


        self.ui.SI_ErrorMsg.clear()
        self.ui.SI_inputUsername.clear()
        self.ui.SI_inputPassword1.clear()
        self.ui.SI_inputPassword2.clear()
        self.ui.SI_dropdownSecurity.setCurrentIndex(0)
        self.ui.SI_checkboxTerm.setChecked(False)


        newAcc = Account(username, password1, security_q, security_a)
        self.ui.innerstackedWidget.setCurrentWidget(self.ui.loginPage)
        addAccount(newAcc)

    def handleLogIn(self) -> Account:
        username = self.ui.LI_inputUsername.text()
        password = self.ui.LI_inputPassword.text()

        isCorrect = checkAccount(username, password)

        self.ui.LI_inputUsername.clear()
        self.ui.LI_inputPassword.clear()

        if isCorrect:
            self.ui.LI_ErrorMsg.setText("")
            self.currentAcc = getAccount(username)
            self.accountChanged()
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            return
        else:
            self.ui.LI_ErrorMsg.setText("Wrong username or password.")
            return

    def handleForgetPW(self):
        username = self.ui.FP_inputUsername.text()

        answer = self.ui.FP_inputSecAnswer.text()

        password1 = self.ui.CP_inputPassword1.text()
        password2 = self.ui.CP_inputPassword2.text()

        if password1 == "" or password2 == "":
            self.ui.CP_errorMsg.setText("Password cannot be empty.")
            return
        if len(password1) <= 5:
            self.ui.CP_errorMsg.setText("Password cannot be less than 5 characters.")
            return
        if " " in password1:
            self.ui.CP_errorMsg.setText("Password cannot has spaces.")
            return
        if password1 != password2:
            self.ui.CP_errorMsg.setText("The typed password doesn't match.")
            return

        if answer == self.currentAcc.security_question:
            thisAcc = getAccount(username)
            thisAcc.password = password1
            editAccount(thisAcc)

            self.ui.stackedWidget.setCurrentWidget(self.ui.loginPage)
        else:
            self.ui.CP_errorMsg.setText("Wrong security answer.")

    def handleChangePW(self):
        answer = self.ui.CP_inputSecAnswer.text()

        password1 = self.ui.CP_inputPassword1.text()
        password2 = self.ui.CP_inputPassword2.text()

        if password1 == "" or password2 == "":
            self.ui.CP_errorMsg.setText("Password cannot be empty.")
            return
        if len(password1) <= 5:
            self.ui.CP_errorMsg.setText("Password cannot be less than 5 characters.")
            return
        if " " in password1:
            self.ui.CP_errorMsg.setText("Password cannot has spaces.")
            return
        if password1 != password2:
            self.ui.CP_errorMsg.setText("The typed password doesn't match.")
            return

        if answer == self.currentAcc.security_question:
            thisAcc = getAccount(self.currentAcc.username)
            thisAcc.password = password1
            editAccount(thisAcc)
            self.ui.stackedWidget.setCurrentWidget(self.ui.loginPage)
        else:
            self.ui.CP_errorMsg.setText("Wrong security answer.")

    def askGemini(self):
        question = self.ui.userChatInput.text()
        self.ui.userChatInput.clear()

        self.addChatFrame(question, False)
        
        # addChats(self.currentAcc.username)

        # Multi-threading
        self.botWorker = botWorker(question)
        self.botWorker.resultReady.connect(self.handleBotAnswer)
        self.botWorker.start()

    def addChatFrame(self, text:str, isBot:bool):
        FRAME = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FRAME.sizePolicy().hasHeightForWidth())
        FRAME.setSizePolicy(sizePolicy)
        FRAME.setMaximumSize(QtCore.QSize(1000, 16777215))
        FRAME.setStyleSheet("background-color: rgb(42, 43, 48); ")
        FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        FRAME.setFrameShadow(QtWidgets.QFrame.Raised)
        
        LAYOUT = QtWidgets.QHBoxLayout(FRAME)
        LAYOUT.setContentsMargins(0, -1, 0, -1)

        if isBot:
            SPACERS = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            LAYOUT.addItem(SPACERS)

            LOGO = QtWidgets.QLabel(FRAME)
            LOGO.setMinimumSize(QtCore.QSize(40, 40))
            LOGO.setMaximumSize(QtCore.QSize(40, 40))
            LOGO.setText("")
            LOGO.setPixmap(QtGui.QPixmap("UI\\../Assets/chatbot/chatbot-blue.png"))
            LOGO.setScaledContents(True)
            LAYOUT.addWidget(LOGO)
        else:
            SPACERS = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
            LAYOUT.addItem(SPACERS)

        LABEL = QtWidgets.QLabel(FRAME)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LABEL.sizePolicy().hasHeightForWidth())
        LABEL.setSizePolicy(sizePolicy)
        LABEL.setMinimumSize(QtCore.QSize(0, 50))
        LABEL.setMaximumSize(QtCore.QSize(4000, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        LABEL.setFont(font)
        LABEL.setStyleSheet(f"""
            color: rgb(255, 255, 255);
            background-color: {"#2A3B47" if isBot else "#6A5ACD"};
            padding-left: 30px;
            padding-right: 25px;
            padding-top: 20px;
            padding-bottom: 20px;
            border-radius: 25px;
        """)
        LABEL.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        LABEL.setWordWrap(True)
        LABEL.setText(f"<html><head/><body><p><span style=\" font-size:11pt;\">{text}</span></p></body></html>")
        LAYOUT.addWidget(LABEL)

        if isBot:
            SPACERS = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
            LAYOUT.addItem(SPACERS)
        else:
            LOGO =  QtWidgets.QLabel(FRAME)
            LOGO.setMinimumSize(QtCore.QSize(40, 40))
            LOGO.setMaximumSize(QtCore.QSize(40, 40))
            LOGO.setText("")
            LOGO.setPixmap(QtGui.QPixmap("UI\\../Assets/chatbot/user2-blue.png"))
            LOGO.setScaledContents(True)
            LAYOUT.addWidget(LOGO)

            SPACERS = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            LAYOUT.addItem(SPACERS)

        self.ui.verticalLayout_9.addWidget(FRAME)
        self.ui.chatHandle.verticalScrollBar().setValue(self.ui.chatHandle.verticalScrollBar().maximum())
    
    def handleBotAnswer(self, answer):
        self.addChatFrame(answer, True)

    def accountChanged(self):
        if self.currentAcc is None:
            # Enable/Disable buttons
            self.ui.loginButton.setEnabled(True)
            self.ui.inputdataButton.setEnabled(False)
            self.ui.visualizeButton.setEnabled(False)
            self.ui.analyzeButton.setEnabled(False)
            self.ui.profileButton.setEnabled(False)
            self.ui.editButton.setEnabled(False)

            # Set opacity effects
            SHOW = QGraphicsOpacityEffect()
            SHOW.setOpacity(1)
            self.ui.loginButton.setGraphicsEffect(SHOW)

            UNSHOW1 = QGraphicsOpacityEffect()
            UNSHOW1.setOpacity(0.5)
            self.ui.inputdataButton.setGraphicsEffect(UNSHOW1)

            UNSHOW2 = QGraphicsOpacityEffect()
            UNSHOW2.setOpacity(0.5)
            self.ui.visualizeButton.setGraphicsEffect(UNSHOW2)

            UNSHOW3 = QGraphicsOpacityEffect()
            UNSHOW3.setOpacity(0.5)
            self.ui.analyzeButton.setGraphicsEffect(UNSHOW3)

            UNSHOW4 = QGraphicsOpacityEffect()
            UNSHOW4.setOpacity(0.5)
            self.ui.profileButton.setGraphicsEffect(UNSHOW4)

            UNSHOW5 = QGraphicsOpacityEffect()
            UNSHOW5.setOpacity(0.5)
            self.ui.editButton.setGraphicsEffect(UNSHOW5)

            self.ui.homeText.setText(f"""
                <html><head/><body>
                    <p>Hi, User!</p>
                    <p>It’s {getDate()}. What would you like to do today?</p>
                    <p>It seems you’re not logged in at the moment. Try logging in or create a new account to get started and enjoy all the features of our app!</p>
                    <p>Need help? Feel free to reach out to our Chatbot<span style=" font-weight:600;"/>if you have any questions or need assistance.</p>
                </body></html>
            """)
            
            return
        else:
            self.ui.loginButton.setEnabled(False)
            self.ui.inputdataButton.setEnabled(True)
            self.ui.profileButton.setEnabled(True)
            self.ui.editButton.setEnabled(True)

            if self.currentAcc.num_transactions != 0:
                self.ui.visualizeButton.setEnabled(True)
                self.ui.analyzeButton.setEnabled(True)
            else:
                self.ui.visualizeButton.setEnabled(False)
                self.ui.analyzeButton.setEnabled(False)

            UNSHOW = QGraphicsOpacityEffect()
            UNSHOW.setOpacity(0.5)
            self.ui.loginButton.setGraphicsEffect(UNSHOW)

            SHOW1 = QGraphicsOpacityEffect()
            SHOW1.setOpacity(1)
            self.ui.profileButton.setGraphicsEffect(SHOW1)

            SHOW2 = QGraphicsOpacityEffect()
            SHOW2.setOpacity(1)
            self.ui.inputdataButton.setGraphicsEffect(SHOW2)

            if self.currentAcc.num_transactions != 0:
                SHOW3 = QGraphicsOpacityEffect()
                SHOW3.setOpacity(1)
                self.ui.visualizeButton.setGraphicsEffect(SHOW3)

                SHOW4 = QGraphicsOpacityEffect()
                SHOW4.setOpacity(1)
                self.ui.analyzeButton.setGraphicsEffect(SHOW4)

                SHOW5 = QGraphicsOpacityEffect()
                SHOW5.setOpacity(1)
                self.ui.editButton.setGraphicsEffect(SHOW5)
            else:
                UNSHOW2 = QGraphicsOpacityEffect()
                UNSHOW2.setOpacity(0.5)
                self.ui.visualizeButton.setGraphicsEffect(UNSHOW2)
                
                UNSHOW3 = QGraphicsOpacityEffect()
                UNSHOW3.setOpacity(0.5)
                self.ui.analyzeButton.setGraphicsEffect(UNSHOW3)

                UNSHOW4 = QGraphicsOpacityEffect()
                UNSHOW4.setOpacity(0.5)
                self.ui.editButton.setGraphicsEffect(UNSHOW4)




        if self.currentAcc.num_transactions != 0:
            df = getTransaction(self.currentAcc)
            self.ED = enrichData(df)
            self.old_data = self.ED.old_data
    
        self.ui.homeText.setText(f"""
            <html><head/><body>
                <p>Hi, {self.currentAcc.username}!</p>
                <p>It is {getDate()}.<br/>What would you like to do?</p>
                <p>Need help? Feel free to reach out to our Chatbot<span style=" font-weight:600;"/>if you have any questions or need assistance.</p>
            </body></html>
            """)
        
        self.ui.PF_usernamePassword.setText(f"""
            <html><head/><body>
                <p><span style=" font-weight:600;">
                    Username
                </span></p>
                
                <p>{self.currentAcc.username}</p>
                
                <p><span style=" font-weight:600;">
                    Password
                </span></p>
                
                <p>{self.currentAcc.password}</p>
            </body></html>
        """)

        self.ui.PF_information.setText(f"""
            <html><head/><body>
                <p><span style=" font-weight:600;">
                    Date Created
                </span></p>
                                       
                <p>{self.currentAcc.created_at}</p>
                                       
                <p><span style=" font-weight:600;">
                    Date Updated
                </span></p>
                                       
                <p>{self.currentAcc.updated_at}</p>
                                       
                <p><span style=" font-weight:600;">
                    Balance
                </span></p>
                                       
                <p>{self.currentAcc.balance}</p>
                                       
                <p><span style=" font-weight:600;">
                    Transaction Uploaded
                </span></p>
                
                <p>{self.currentAcc.num_transactions}</p>
            </body></html>
        """)

if __name__ == "__main__":

    os.system("cls" if os.name == "nt" else "clear")

    global counter, jumper
    counter = 0
    jumper = 0

    global start

    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    app.exec_()

    updateTimesOpened()
    updateTimeSpent(start)
    
    sys.exit()