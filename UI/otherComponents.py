from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Notification(QWidget):
    def __init__(self, text: str, type: int, timer: int = 1000):
        super().__init__()
        self.text = text
        self.type = type
        self.timer_duration = timer
        self.initUI()

    def initUI(self):
        label = QLabel(self)
        font = QFont()
        font.setFamily("Poppins")
        font.setPixelSize(11)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        label.setWordWrap(True)
        label.setText(self.text)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.setWindowFlags(self.windowFlags() | 
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        
        self.setGeometry(300, 300, 250, 150)
        self.show()

        QtCore.QTimer.singleShot(self.timer_duration, self.close)