import sys
import os

import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

from Intro import Ui_Intro
from Menu import Ui_Menu
from Holder import Ui_Holder

os.system("cls" if os.name == "nt" else "clear")

class cIntro(QDialog, Ui_Intro):
    def __init__(self):
        super(cIntro, self).__init__()
        self.setupUi(self)

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, self.width(), self.height())

        new_font_size = max(self.width() // 22, 24)
        font = QFont("Calibri Light", new_font_size)
        self.label.setFont(font)

        new_font_size = max(self.width() // 48, 11)
        font = QFont("Calibri Light", new_font_size)
        self.label_2.setFont(font)

        super(cIntro, self).resizeEvent(event)

    def showEvent(self, event):
        super(cIntro, self).showEvent(event)
        self.mainAnimation()

    def mainAnimation(self):
        text1 = "My Project"
        text2 = """Created By:          

Jonathan Edward Charles De Fretes     
Davin Nazhif Wilviadli     
Muhammad Farhan Hanafi
        """

        for i in range(len(text1) + 1):
            QTimer.singleShot(70 * i, lambda i=i: self.label.setText(text1[:i]))

        total_duration1 = 70 * (len(text1) + 1) + 1000

        for i in range(len(text2) + 1):
            QTimer.singleShot(total_duration1 + 50 * i, lambda i=i: self.label_2.setText(text2[:i]))

        total_duration2 = total_duration1 + 50 * (len(text2) + 1) + 1000
        QTimer.singleShot(total_duration2, self.nextPage)

    def nextPage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class cMenu(QDialog, Ui_Menu):
    def __init__(self):
        super(cMenu, self).__init__()
        self.setupUi(self)

class cHolder(QStackedWidget, Ui_Holder):
    def __init__(self):
        super(cHolder, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    _intro = cIntro()
    _menu = cMenu()
    widget = cHolder()

    widget.addWidget(_intro)
    widget.addWidget(_menu)
    widget.show()

    sys.exit(app.exec_())
