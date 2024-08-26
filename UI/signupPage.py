# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Davin Nazhif\Documents\GitHub\pfm\UI\signupPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_signupPage(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(522, 922)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.signupFrame = QtWidgets.QFrame(Form)
        self.signupFrame.setMinimumSize(QtCore.QSize(500, 900))
        self.signupFrame.setMaximumSize(QtCore.QSize(700, 1000))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.signupFrame.setFont(font)
        self.signupFrame.setStyleSheet("#signupFrame{\n"
"    background-color: rgb(42, 43, 48);\n"
"    border-radius: 15px;       \n"
"       padding-left: 15px;      \n"
"       padding-right: 15px;       \n"
"    padding-top: 25px;          \n"
"    padding-bottom: 25px; \n"
"}\n"
"QLabel{\n"
"    padding-left:5px;\n"
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
"    color:#808390;\n"
"}\n"
"#login{\n"
"    color:rgb(255, 255, 255);\n"
"    background-color: rgb(84, 86, 95);\n"
"    border-radius:15px;\n"
"    height:30px;\n"
"}\n"
"QComboBox {\n"
"    color: white;                        /* Warna teks combobox */\n"
"    background-color: #333333;           /* Warna latar belakang combobox */\n"
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.signupFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.signupFrame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.haveAcc = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.haveAcc.setFont(font)
        self.haveAcc.setStyleSheet("padding-left:0px;")
        self.haveAcc.setObjectName("haveAcc")
        self.horizontalLayout_3.addWidget(self.haveAcc)
        self.login = QtWidgets.QPushButton(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.login.setFont(font)
        self.login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login.setObjectName("login")
        self.horizontalLayout_3.addWidget(self.login)
        self.gridLayout_2.addWidget(self.frame_4, 16, 0, 1, 1)
        self.signuperrorMsg = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        self.signuperrorMsg.setFont(font)
        self.signuperrorMsg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.signuperrorMsg.setStyleSheet("color:rgb(42, 43, 48);")
        self.signuperrorMsg.setObjectName("signuperrorMsg")
        self.gridLayout_2.addWidget(self.signuperrorMsg, 11, 0, 1, 1)
        self.termAgree = QtWidgets.QCheckBox(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.termAgree.setFont(font)
        self.termAgree.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.termAgree.setObjectName("termAgree")
        self.gridLayout_2.addWidget(self.termAgree, 12, 0, 1, 1)
        self.signup = QtWidgets.QPushButton(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.signup.setFont(font)
        self.signup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signup.setObjectName("signup")
        self.gridLayout_2.addWidget(self.signup, 14, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.regUsername = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.regUsername.setFont(font)
        self.regUsername.setObjectName("regUsername")
        self.gridLayout_2.addWidget(self.regUsername, 2, 0, 1, 1)
        self.signupHeader = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)
        self.signupHeader.setFont(font)
        self.signupHeader.setObjectName("signupHeader")
        self.gridLayout_2.addWidget(self.signupHeader, 0, 0, 1, 1)
        self.inputregUsername = QtWidgets.QLineEdit(self.signupFrame)
        self.inputregUsername.setText("")
        self.inputregUsername.setObjectName("inputregUsername")
        self.gridLayout_2.addWidget(self.inputregUsername, 3, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.signupFrame)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 10, 0, 1, 1)
        self.regPw = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.regPw.setFont(font)
        self.regPw.setObjectName("regPw")
        self.gridLayout_2.addWidget(self.regPw, 4, 0, 1, 1)
        self.inputregPw = QtWidgets.QLineEdit(self.signupFrame)
        self.inputregPw.setText("")
        self.inputregPw.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.inputregPw.setObjectName("inputregPw")
        self.gridLayout_2.addWidget(self.inputregPw, 5, 0, 1, 1)
        self.security = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.security.setFont(font)
        self.security.setStyleSheet("")
        self.security.setObjectName("security")
        self.gridLayout_2.addWidget(self.security, 8, 0, 1, 1)
        self.reinputregPw = QtWidgets.QLineEdit(self.signupFrame)
        self.reinputregPw.setText("")
        self.reinputregPw.setObjectName("reinputregPw")
        self.gridLayout_2.addWidget(self.reinputregPw, 6, 0, 1, 1)
        self.secQuestion = QtWidgets.QComboBox(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.secQuestion.setFont(font)
        self.secQuestion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.secQuestion.setStyleSheet("background-color: rgb(128, 131, 144);")
        self.secQuestion.setEditable(False)
        self.secQuestion.setCurrentText("")
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
        self.gridLayout_2.addWidget(self.secQuestion, 9, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 15, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.signupFrame)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 13, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.signupFrame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.secQuestion.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.haveAcc.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#808390;\">Already have an account?</span></p></body></html>"))
        self.login.setText(_translate("Form", "Login"))
        self.signuperrorMsg.setText(_translate("Form", "<html><head/><body><p align=\"right\">*Password Doesn\'t Match</p></body></html>"))
        self.termAgree.setText(_translate("Form", "I accept the Terms of Service and Privacy Policy."))
        self.signup.setText(_translate("Form", "Sign up"))
        self.regUsername.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#808390;\">Username</span><span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.signupHeader.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; color:#fedd3b;\">Build your wealth.</span></p><p><span style=\" font-size:16pt; color:#808390;\">Create your PFM account</span></p></body></html>"))
        self.inputregUsername.setPlaceholderText(_translate("Form", "Create your username..."))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Write your answer..."))
        self.regPw.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#808390;\">Password</span><span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.inputregPw.setPlaceholderText(_translate("Form", "Create your password..."))
        self.security.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#808390;\">Security</span><span style=\" color:#ea0003;\">*</span></p></body></html>"))
        self.reinputregPw.setPlaceholderText(_translate("Form", "Re-enter your password..."))
        self.secQuestion.setItemText(1, _translate("Form", "  Birthplace"))
        self.secQuestion.setItemText(2, _translate("Form", "  Favorite book"))
        self.secQuestion.setItemText(3, _translate("Form", "  Favorite color"))
        self.secQuestion.setItemText(4, _translate("Form", "  Favorite food"))
        self.secQuestion.setItemText(5, _translate("Form", "  Favorite movie"))
        self.secQuestion.setItemText(6, _translate("Form", "  Favorite sport"))
        self.secQuestion.setItemText(7, _translate("Form", "  Favorite band"))
        self.secQuestion.setItemText(8, _translate("Form", "  Pet\'s name"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#808390;\">Fields marked with (</span><span style=\" color:#ea0003;\">*</span><span style=\" color:#808390;\">) are required.</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_signupPage()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
