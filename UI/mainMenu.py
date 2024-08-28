# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Davin Nazhif\Documents\GitHub\pfm\UI\mainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 766)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mainMenu = QtWidgets.QWidget(self.centralwidget)
        self.mainMenu.setStyleSheet("background-color: #23272A")
        self.mainMenu.setObjectName("mainMenu")
        self.gridLayout = QtWidgets.QGridLayout(self.mainMenu)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.mainMenu)
        self.stackedWidget.setObjectName("stackedWidget")
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.label = QtWidgets.QLabel(self.home)
        self.label.setGeometry(QtCore.QRect(290, 250, 401, 191))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.home)
        self.loginsignup = QtWidgets.QWidget()
        self.loginsignup.setObjectName("loginsignup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.loginsignup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.innerstackedWidget = QtWidgets.QStackedWidget(self.loginsignup)
        self.innerstackedWidget.setMinimumSize(QtCore.QSize(630, 700))
        self.innerstackedWidget.setMaximumSize(QtCore.QSize(1000, 1000))
        self.innerstackedWidget.setObjectName("innerstackedWidget")
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setStyleSheet("")
        self.loginPage.setObjectName("loginPage")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.loginPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.loginFrame = QtWidgets.QFrame(self.loginPage)
        self.loginFrame.setMinimumSize(QtCore.QSize(500, 630))
        self.loginFrame.setMaximumSize(QtCore.QSize(1000, 700))
        self.loginFrame.setStyleSheet("#loginFrame{\n"
"    background-color: rgb(42, 43, 48);       \n"
"       padding-left: 15px;      \n"
"       padding-right: 20px;       \n"
"    padding-top: 25px;          \n"
"    padding-bottom: 25px;\n"
"    border-radius: 15px;      \n"
"}\n"
"#username, #password{\n"
"    padding-top:25px;\n"
"}\n"
"QLabel{\n"
"    background-color:none;\n"
"    padding:5px;\n"
"}\n"
"QLineEdit{\n"
"    height:50px;\n"
"    padding: 1px 15 px;\n"
"    background-color: rgb(42, 43, 48);\n"
"    border: 1px solid rgba(84,86,95,255);\n"
"    border-radius: 10px;\n"
"    color:rgb(255, 255, 255);\n"
"}\n"
"#signin{\n"
"    background-color: rgb(254, 221, 59);    \n"
"    border-radius:5px;\n"
"    height:50px;\n"
"}\n"
"#createAcc{\n"
"    color:rgb(255, 255, 255);\n"
"    background-color: rgb(84, 86, 95);\n"
"    border-radius:15px;\n"
"    height:30px;\n"
"}\n"
"#forgotPW{\n"
"    background-color:rgb(42,43,48);\n"
"    color:#808390;\n"
"    border-radius:15px;\n"
"    height:30px;\n"
"}\n"
"#username, #password, #noAcc{\n"
"    color: rgb(128, 131, 144);\n"
"    font-family: Poppins;\n"
"}\n"
"#errorMsg{\n"
"    color: rgb(42, 43, 48);\n"
"    font-family: Poppins;\n"
"}\n"
"#frame, #frame_2{\n"
"background-color: rgb(42, 43, 48);\n"
"}")
        self.loginFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.loginFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.loginFrame.setObjectName("loginFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.loginFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.username = QtWidgets.QLabel(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.username.setFont(font)
        self.username.setObjectName("username")
        self.gridLayout_4.addWidget(self.username, 1, 0, 1, 1)
        self.password = QtWidgets.QLabel(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.gridLayout_4.addWidget(self.password, 3, 0, 1, 1)
        self.inputUsername = QtWidgets.QLineEdit(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.inputUsername.setFont(font)
        self.inputUsername.setObjectName("inputUsername")
        self.gridLayout_4.addWidget(self.inputUsername, 2, 0, 1, 1)
        self.inputPw = QtWidgets.QLineEdit(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.inputPw.setFont(font)
        self.inputPw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPw.setObjectName("inputPw")
        self.gridLayout_4.addWidget(self.inputPw, 4, 0, 1, 1)
        self.signin = QtWidgets.QPushButton(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.signin.setFont(font)
        self.signin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signin.setObjectName("signin")
        self.gridLayout_4.addWidget(self.signin, 6, 0, 1, 1)
        self.loginHeader = QtWidgets.QLabel(self.loginFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(13)
        self.loginHeader.setFont(font)
        self.loginHeader.setObjectName("loginHeader")
        self.gridLayout_4.addWidget(self.loginHeader, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(553, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 7, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.loginFrame)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.forgotPW = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.forgotPW.setFont(font)
        self.forgotPW.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forgotPW.setObjectName("forgotPW")
        self.horizontalLayout_2.addWidget(self.forgotPW)
        spacerItem1 = QtWidgets.QSpacerItem(589, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.errorMsg = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        self.errorMsg.setFont(font)
        self.errorMsg.setObjectName("errorMsg")
        self.horizontalLayout_2.addWidget(self.errorMsg)
        self.gridLayout_4.addWidget(self.frame, 5, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.loginFrame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.noAcc = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.noAcc.setFont(font)
        self.noAcc.setObjectName("noAcc")
        self.horizontalLayout_3.addWidget(self.noAcc)
        self.createAcc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.createAcc.setFont(font)
        self.createAcc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createAcc.setObjectName("createAcc")
        self.horizontalLayout_3.addWidget(self.createAcc)
        self.gridLayout_4.addWidget(self.frame_2, 8, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.loginFrame)
        self.innerstackedWidget.addWidget(self.loginPage)
        self.signupPage = QtWidgets.QWidget()
        self.signupPage.setStyleSheet("QScrollArea {\n"
"    border: 10px solid rgb(42, 43, 48);; /* Set the border color and width */\n"
"    border-radius: 15px; /* Optional: Add some rounding to the corners */\n"
"    background-color:  rgb(42, 43, 48); /* Ensure the background matches your theme */\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background-color: #2C2F33;\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #555;\n"
"    min-height: 20px;\n"
"    border-radius: 5px;\n"
"    border: 2px solid #2C2F33;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background-color: #888;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.signupPage.setObjectName("signupPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.signupPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.signupPage)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollBar = QtWidgets.QWidget()
        self.scrollBar.setGeometry(QtCore.QRect(0, -168, 576, 900))
        self.scrollBar.setStyleSheet("")
        self.scrollBar.setObjectName("scrollBar")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollBar)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.signupFrame = QtWidgets.QFrame(self.scrollBar)
        self.signupFrame.setMinimumSize(QtCore.QSize(500, 900))
        self.signupFrame.setStyleSheet("#signupFrame{\n"
"    background-color: rgb(42, 43, 48);    \n"
"       padding-left: 5px;      \n"
"       padding-right: 5px;       \n"
"    padding-top: 25px;          \n"
"    padding-bottom: 25px;\n"
"}\n"
"#backtoLogin{\n"
"    color:rgb(255, 255, 255);\n"
"    background-color: rgb(84, 86, 95);\n"
"    border-radius:15px;\n"
"    height:30px;\n"
"}\n"
"QLabel{\n"
"    background-color: rgb(42, 43, 48);\n"
"    padding-left:5px;\n"
"}\n"
"#frame_3{\n"
"    background-color: rgb(42, 43, 48);\n"
"}\n"
"#regUsername, #regPw, #security, #signuperrorMsg, #requiredField, #haveAcc{\n"
"    color:#808390;\n"
"    font-family: Poppins;\n"
"}\n"
"\n"
"#regUsername, #regPw, #security{\n"
"    padding-top:25px;\n"
"}\n"
"QLineEdit{\n"
"    height:50px;\n"
"    padding: 1px 15 px;\n"
"    background-color: rgb(42, 43, 48);\n"
"    border: 1px solid rgba(84,86,95,255);\n"
"    border-radius: 10px;\n"
"    color:rgb(255, 255, 255);\n"
"    font-family: Poppins;\n"
"    font-size:15px;\n"
"}\n"
"#signup{\n"
"    background-color: rgb(254, 221, 59);    \n"
"    border-radius:5px;\n"
"    height:50px;\n"
"}\n"
"#termAgree{\n"
"    background-color: rgb(42, 43, 48);\n"
"    color:#808390;\n"
"}\n"
"QComboBox {\n"
"    color: white;                        /* Warna teks combobox */\n"
"    background-color:  rgb(128, 131, 144);           /* Warna latar belakang combobox */\n"
"    border: 1px solid #555555;           /* Warna border combobox */\n"
"    border-radius: 5px;                  /* Membuat sudut rounded */\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    color: white;                        /* Warna teks dropdown */\n"
"    background-color: #333333;           /* Warna latar belakang dropdown */\n"
"    selection-background-color: #fedd3b; /* Warna latar belakang item yang dipilih*/\n"
"    selection-color: black;              /* Warna teks item yang dipilih */\n"
"    border: 1px solid #555555;          /* Warna border dropdown */\n"
"}\n"
"")
        self.signupFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signupFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signupFrame.setObjectName("signupFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.signupFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.signupHeader = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(13)
        self.signupHeader.setFont(font)
        self.signupHeader.setObjectName("signupHeader")
        self.verticalLayout_4.addWidget(self.signupHeader)
        self.regUsername = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.regUsername.setFont(font)
        self.regUsername.setObjectName("regUsername")
        self.verticalLayout_4.addWidget(self.regUsername)
        self.inputregUsername = QtWidgets.QLineEdit(self.signupFrame)
        self.inputregUsername.setObjectName("inputregUsername")
        self.verticalLayout_4.addWidget(self.inputregUsername)
        self.regPw = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.regPw.setFont(font)
        self.regPw.setObjectName("regPw")
        self.verticalLayout_4.addWidget(self.regPw)
        self.inputregPw = QtWidgets.QLineEdit(self.signupFrame)
        self.inputregPw.setStyleSheet("")
        self.inputregPw.setObjectName("inputregPw")
        self.verticalLayout_4.addWidget(self.inputregPw)
        self.reinputregPw = QtWidgets.QLineEdit(self.signupFrame)
        self.reinputregPw.setObjectName("reinputregPw")
        self.verticalLayout_4.addWidget(self.reinputregPw)
        self.security = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.security.setFont(font)
        self.security.setStyleSheet("")
        self.security.setObjectName("security")
        self.verticalLayout_4.addWidget(self.security)
        self.secQuestion = QtWidgets.QComboBox(self.signupFrame)
        self.secQuestion.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.secQuestion.setFont(font)
        self.secQuestion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.secQuestion.setStyleSheet("")
        self.secQuestion.setObjectName("secQuestion")
        self.secQuestion.addItem("")
        self.secQuestion.setItemText(0, "")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.secQuestion.addItem("")
        self.verticalLayout_4.addWidget(self.secQuestion)
        self.secAnswer = QtWidgets.QLineEdit(self.signupFrame)
        self.secAnswer.setObjectName("secAnswer")
        self.verticalLayout_4.addWidget(self.secAnswer)
        self.signuperrorMsg = QtWidgets.QLabel(self.signupFrame)
        self.signuperrorMsg.setMinimumSize(QtCore.QSize(0, 0))
        self.signuperrorMsg.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.signuperrorMsg.setFont(font)
        self.signuperrorMsg.setStyleSheet(" color:rgb(42, 43, 48);\n"
"")
        self.signuperrorMsg.setObjectName("signuperrorMsg")
        self.verticalLayout_4.addWidget(self.signuperrorMsg)
        self.termAgree = QtWidgets.QCheckBox(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.termAgree.setFont(font)
        self.termAgree.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.termAgree.setStyleSheet("padding-left:7px;")
        self.termAgree.setObjectName("termAgree")
        self.verticalLayout_4.addWidget(self.termAgree)
        self.requiredField = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.requiredField.setFont(font)
        self.requiredField.setObjectName("requiredField")
        self.verticalLayout_4.addWidget(self.requiredField)
        self.signup = QtWidgets.QPushButton(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.signup.setFont(font)
        self.signup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signup.setObjectName("signup")
        self.verticalLayout_4.addWidget(self.signup)
        self.frame_3 = QtWidgets.QFrame(self.signupFrame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.haveAcc = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.haveAcc.setFont(font)
        self.haveAcc.setStyleSheet("padding:0px;")
        self.haveAcc.setObjectName("haveAcc")
        self.horizontalLayout.addWidget(self.haveAcc)
        self.backtoLogin = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.backtoLogin.setFont(font)
        self.backtoLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backtoLogin.setStyleSheet("")
        self.backtoLogin.setObjectName("backtoLogin")
        self.horizontalLayout.addWidget(self.backtoLogin)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.gridLayout_5.addWidget(self.signupFrame, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollBar)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.innerstackedWidget.addWidget(self.signupPage)
        self.changePW = QtWidgets.QWidget()
        self.changePW.setStyleSheet("")
        self.changePW.setObjectName("changePW")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.changePW)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.changepwFrame = QtWidgets.QFrame(self.changePW)
        self.changepwFrame.setStyleSheet("#changepwFrame{\n"
"    background-color: rgb(42, 43, 48);\n"
"       padding-left: 15px;      \n"
"       padding-right: 20px;       \n"
"    padding-top: 25px;          \n"
"    padding-bottom: 25px;\n"
"    border-radius: 15px;      \n"
"}\n"
"#frame_5{\n"
"    background-color: rgb(42, 43, 48);\n"
"}\n"
"QLineEdit{\n"
"    height:50px;\n"
"    padding: 1px 15 px;\n"
"    background-color: rgb(42, 43, 48);\n"
"    border: 1px solid rgba(84,86,95,255);\n"
"    border-radius: 10px;\n"
"    color:rgb(255, 255, 255);\n"
"    font-family: Poppins;\n"
"    font-size:15px;\n"
"}\n"
"QLabel{\n"
"    background-color: rgb(42, 43, 48);\n"
"    padding-left:5px;\n"
"}\n"
"#savePw{\n"
"    background-color: #FFD700;    \n"
"    border-radius:5px;\n"
"    height:50px;\n"
"}\n"
"#secQuestionLabel, #resetPw, #whatuWaiting{\n"
"    color:#808390;\n"
"    font-family: Poppins;\n"
"}\n"
"#secQuestionLabel, #resetPw{\n"
"    padding-top:25px;\n"
"}\n"
"#backtoLogin_2{\n"
"    color:rgb(255, 255, 255);\n"
"    background-color: rgb(84, 86, 95);\n"
"    border-radius:15px;\n"
"    height:30px;\n"
"}\n"
"QComboBox {\n"
"    color: white;                        /* Warna teks combobox */\n"
"    background-color:rgb(128, 131, 144);           /* Warna latar belakang combobox */\n"
"    border: 1px solid #555555;           /* Warna border combobox */\n"
"    border-radius: 5px;                  /* Membuat sudut rounded */\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    color: white;                        /* Warna teks dropdown */\n"
"    background-color: #333333;           /* Warna latar belakang dropdown */\n"
"    selection-background-color: #fedd3b; /* Warna latar belakang item yang dipilih*/\n"
"    selection-color: black;              /* Warna teks item yang dipilih */\n"
"    border: 1px solid #555555;          /* Warna border dropdown */\n"
"}")
        self.changepwFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.changepwFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.changepwFrame.setObjectName("changepwFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.changepwFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.changepwHeader = QtWidgets.QLabel(self.changepwFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        self.changepwHeader.setFont(font)
        self.changepwHeader.setObjectName("changepwHeader")
        self.verticalLayout_5.addWidget(self.changepwHeader)
        self.secQuestionLabel = QtWidgets.QLabel(self.changepwFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.secQuestionLabel.setFont(font)
        self.secQuestionLabel.setObjectName("secQuestionLabel")
        self.verticalLayout_5.addWidget(self.secQuestionLabel)
        self.secQuestion_2 = QtWidgets.QComboBox(self.changepwFrame)
        self.secQuestion_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.secQuestion_2.setFont(font)
        self.secQuestion_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.secQuestion_2.setStyleSheet("")
        self.secQuestion_2.setObjectName("secQuestion_2")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.setItemText(0, "")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.secQuestion_2.addItem("")
        self.verticalLayout_5.addWidget(self.secQuestion_2)
        self.secAnswer_2 = QtWidgets.QLineEdit(self.changepwFrame)
        self.secAnswer_2.setObjectName("secAnswer_2")
        self.verticalLayout_5.addWidget(self.secAnswer_2)
        self.resetPw = QtWidgets.QLabel(self.changepwFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.resetPw.setFont(font)
        self.resetPw.setObjectName("resetPw")
        self.verticalLayout_5.addWidget(self.resetPw)
        self.enternewPw = QtWidgets.QLineEdit(self.changepwFrame)
        self.enternewPw.setObjectName("enternewPw")
        self.verticalLayout_5.addWidget(self.enternewPw)
        self.reenternewPw = QtWidgets.QLineEdit(self.changepwFrame)
        self.reenternewPw.setObjectName("reenternewPw")
        self.verticalLayout_5.addWidget(self.reenternewPw)
        self.succesMsg = QtWidgets.QLabel(self.changepwFrame)
        self.succesMsg.setMinimumSize(QtCore.QSize(0, 25))
        self.succesMsg.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.succesMsg.setFont(font)
        self.succesMsg.setObjectName("succesMsg")
        self.verticalLayout_5.addWidget(self.succesMsg)
        self.savePw = QtWidgets.QPushButton(self.changepwFrame)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.savePw.setFont(font)
        self.savePw.setObjectName("savePw")
        self.verticalLayout_5.addWidget(self.savePw)
        self.frame_5 = QtWidgets.QFrame(self.changepwFrame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.whatuWaiting = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.whatuWaiting.setFont(font)
        self.whatuWaiting.setObjectName("whatuWaiting")
        self.horizontalLayout_4.addWidget(self.whatuWaiting)
        self.backtoLogin_2 = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.backtoLogin_2.setFont(font)
        self.backtoLogin_2.setObjectName("backtoLogin_2")
        self.horizontalLayout_4.addWidget(self.backtoLogin_2)
        self.verticalLayout_5.addWidget(self.frame_5)
        self.gridLayout_6.addWidget(self.changepwFrame, 0, 0, 1, 1)
        self.innerstackedWidget.addWidget(self.changePW)
        self.gridLayout_2.addWidget(self.innerstackedWidget, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.loginsignup)
        self.inputData = QtWidgets.QWidget()
        self.inputData.setObjectName("inputData")
        self.label_3 = QtWidgets.QLabel(self.inputData)
        self.label_3.setGeometry(QtCore.QRect(204, 165, 521, 361))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.stackedWidget.addWidget(self.inputData)
        self.showData = QtWidgets.QWidget()
        self.showData.setObjectName("showData")
        self.label_4 = QtWidgets.QLabel(self.showData)
        self.label_4.setGeometry(QtCore.QRect(250, 300, 461, 161))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.stackedWidget.addWidget(self.showData)
        self.chatBot = QtWidgets.QWidget()
        self.chatBot.setObjectName("chatBot")
        self.label_5 = QtWidgets.QLabel(self.chatBot)
        self.label_5.setGeometry(QtCore.QRect(290, 320, 291, 101))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.stackedWidget.addWidget(self.chatBot)
        self.profile = QtWidgets.QWidget()
        self.profile.setObjectName("profile")
        self.label_6 = QtWidgets.QLabel(self.profile)
        self.label_6.setGeometry(QtCore.QRect(320, 230, 231, 211))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.stackedWidget.addWidget(self.profile)
        self.about = QtWidgets.QWidget()
        self.about.setObjectName("about")
        self.label_7 = QtWidgets.QLabel(self.about)
        self.label_7.setGeometry(QtCore.QRect(330, 260, 261, 221))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.stackedWidget.addWidget(self.about)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.mainMenu, 0, 1, 1, 1)
        self.menuBar = QtWidgets.QWidget(self.centralwidget)
        self.menuBar.setMaximumSize(QtCore.QSize(90, 16777215))
        self.menuBar.setObjectName("menuBar")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.menuBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.homeButton = QtWidgets.QPushButton(self.menuBar)
        self.homeButton.setStyleSheet("")
        self.homeButton.setObjectName("homeButton")
        self.verticalLayout.addWidget(self.homeButton)
        self.loginButton = QtWidgets.QPushButton(self.menuBar)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout.addWidget(self.loginButton)
        self.inputdataButton = QtWidgets.QPushButton(self.menuBar)
        self.inputdataButton.setObjectName("inputdataButton")
        self.verticalLayout.addWidget(self.inputdataButton)
        self.showdatabutton = QtWidgets.QPushButton(self.menuBar)
        self.showdatabutton.setObjectName("showdatabutton")
        self.verticalLayout.addWidget(self.showdatabutton)
        self.chatbotButton = QtWidgets.QPushButton(self.menuBar)
        self.chatbotButton.setObjectName("chatbotButton")
        self.verticalLayout.addWidget(self.chatbotButton)
        self.profileButton = QtWidgets.QPushButton(self.menuBar)
        self.profileButton.setObjectName("profileButton")
        self.verticalLayout.addWidget(self.profileButton)
        self.aboutButton = QtWidgets.QPushButton(self.menuBar)
        self.aboutButton.setObjectName("aboutButton")
        self.verticalLayout.addWidget(self.aboutButton)
        self.gridLayout_3.addWidget(self.menuBar, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.innerstackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Home"))
        self.username.setText(_translate("MainWindow", "Username"))
        self.password.setText(_translate("MainWindow", "Password"))
        self.inputUsername.setPlaceholderText(_translate("MainWindow", "Please enter your username..."))
        self.inputPw.setPlaceholderText(_translate("MainWindow", "Please enter yout password..."))
        self.signin.setText(_translate("MainWindow", "Log in"))
        self.loginHeader.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; color:#fedd3b;\">Take control of your finances.</span></p><p><span style=\" font-size:20pt; color:#808390;\">Log in to your PFM account</span></p></body></html>"))
        self.forgotPW.setText(_translate("MainWindow", "Forgot Password?"))
        self.errorMsg.setText(_translate("MainWindow", "*Incorrect Password"))
        self.noAcc.setText(_translate("MainWindow", "Don\'t Have an Account Yet?"))
        self.createAcc.setText(_translate("MainWindow", "Create"))
        self.signupHeader.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; color:#fedd3b;\">Build your wealth.</span></p><p><span style=\" font-size:20pt; color:#808390;\">Create your PFM account</span></p></body></html>"))
        self.regUsername.setText(_translate("MainWindow", "<html><head/><body><p>Username<span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.inputregUsername.setPlaceholderText(_translate("MainWindow", "Create your username..."))
        self.regPw.setText(_translate("MainWindow", "<html><head/><body><p>Password<span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.inputregPw.setPlaceholderText(_translate("MainWindow", "Create your password..."))
        self.reinputregPw.setPlaceholderText(_translate("MainWindow", "Re-enter your password..."))
        self.security.setText(_translate("MainWindow", "<html><head/><body><p>Security<span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.secQuestion.setItemText(1, _translate("MainWindow", "   Birthplace"))
        self.secQuestion.setItemText(2, _translate("MainWindow", "   Favorite book"))
        self.secQuestion.setItemText(3, _translate("MainWindow", "   Favorite color"))
        self.secQuestion.setItemText(4, _translate("MainWindow", "   Favorite food"))
        self.secQuestion.setItemText(5, _translate("MainWindow", "   Favorite movie"))
        self.secQuestion.setItemText(6, _translate("MainWindow", "   Favorite sport"))
        self.secQuestion.setItemText(7, _translate("MainWindow", "   Favorite band"))
        self.secQuestion.setItemText(8, _translate("MainWindow", "   Pet\'s name"))
        self.secAnswer.setPlaceholderText(_translate("MainWindow", "Write your answer..."))
        self.signuperrorMsg.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">*Password Doesn\'t Match</p></body></html>"))
        self.termAgree.setText(_translate("MainWindow", "I accept the Terms of Service and Privacy Policy"))
        self.requiredField.setText(_translate("MainWindow", "Fields marked with (*) are requierd."))
        self.signup.setText(_translate("MainWindow", "Sign up"))
        self.haveAcc.setText(_translate("MainWindow", "Already Have an Account?"))
        self.backtoLogin.setText(_translate("MainWindow", "Log in"))
        self.changepwHeader.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; color:#fedd3b;\">Protect your finances.</span></p><p><span style=\" font-size:20pt; color:#808390;\">Enhance your protection.</span></p></body></html>"))
        self.secQuestionLabel.setText(_translate("MainWindow", "Security Question"))
        self.secQuestion_2.setItemText(1, _translate("MainWindow", "   Birthplace"))
        self.secQuestion_2.setItemText(2, _translate("MainWindow", "   Favorite book"))
        self.secQuestion_2.setItemText(3, _translate("MainWindow", "   Favorite color"))
        self.secQuestion_2.setItemText(4, _translate("MainWindow", "   Favorite food"))
        self.secQuestion_2.setItemText(5, _translate("MainWindow", "   Favorite movie"))
        self.secQuestion_2.setItemText(6, _translate("MainWindow", "   Favorite sport"))
        self.secQuestion_2.setItemText(7, _translate("MainWindow", "   Favorite band"))
        self.secQuestion_2.setItemText(8, _translate("MainWindow", "   Pet\'s name"))
        self.secAnswer_2.setPlaceholderText(_translate("MainWindow", "Write your answer..."))
        self.resetPw.setText(_translate("MainWindow", "Reset Password"))
        self.enternewPw.setPlaceholderText(_translate("MainWindow", "Create your new password..."))
        self.reenternewPw.setPlaceholderText(_translate("MainWindow", "Enter your new password..."))
        self.succesMsg.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" color:#2a2b30;\">*Passwords don\'t match</span></p></body></html>"))
        self.savePw.setText(_translate("MainWindow", "Save"))
        self.whatuWaiting.setText(_translate("MainWindow", "What Are You Waiting For?"))
        self.backtoLogin_2.setText(_translate("MainWindow", "Back to Log In"))
        self.label_3.setText(_translate("MainWindow", "Input Data"))
        self.label_4.setText(_translate("MainWindow", "Show Data"))
        self.label_5.setText(_translate("MainWindow", "Chatbot"))
        self.label_6.setText(_translate("MainWindow", "Profile"))
        self.label_7.setText(_translate("MainWindow", "About"))
        self.homeButton.setText(_translate("MainWindow", "Home"))
        self.loginButton.setText(_translate("MainWindow", "Login/Signup"))
        self.inputdataButton.setText(_translate("MainWindow", "Input Data"))
        self.showdatabutton.setText(_translate("MainWindow", "Show Data"))
        self.chatbotButton.setText(_translate("MainWindow", "Chat Bot"))
        self.profileButton.setText(_translate("MainWindow", "Profile"))
        self.aboutButton.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
