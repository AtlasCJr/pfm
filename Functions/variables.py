from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from Functions.chats import getBotAnswer

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from PyQt5 import QtWidgets


class Account:
    def __init__(self, username: str, 
                 password: str, 
                 security_question:int, 
                 security_answer:str, 
                 created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 balance:int = 0,
                 num_transactions:int = 0
                ) -> None:
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.created_at = created_at
        self.updated_at = updated_at
        self.balance = balance
        self.num_transactions = num_transactions

    def summary(self):
        print(f"{'Username':>15}: {self.username}")
        print(f"{'Password':>15}: {self.password}")
        print(f"{'Date Created':>15}: {self.created_at}")
        print(f"{'Date Updated':>15}: {self.updated_at}")
        print(f"{'Balance':>15}: {self.balance}")

class botWorker(QThread):
    resultReady = pyqtSignal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        bot_answer = getBotAnswer(self.question)
        self.resultReady.emit(bot_answer)

class Canvas(FigureCanvas):
    def __init__(self, parent=None, figsize=(12, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.updateGeometry()

class enrichedData:
    def __init__(self, old_data: pd.DataFrame, data: pd.DataFrame, figsize: tuple[int, int] = (20, 10)) -> None:
        self.old_data = old_data
        self.data = data
        self.figsize = figsize

    def plotAll(self, RANGE1: str, RANGE2: str, displacement: tuple[int, ...], parent):
        canvas = Canvas(parent, figsize=self.figsize)
        
        if RANGE1 != "YEAR":
            last_data = self.data['Features', RANGE2].iloc[-1] - displacement
            curData = self.data[self.data['Features', RANGE2] == last_data]
            curData = curData.groupby(self.data['Features'][RANGE1]).sum()

            canvas.ax.text(0.5, 1.01, f"{RANGE2.title()} {last_data}", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=15)
        else:
            curData = self.data.groupby(self.data['Features']['YEAR']).sum()
            last_data = curData.index[-1]

            canvas.ax.text(0.5, 1.04, f"All Year", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=10)

        canvas.ax.set_xlabel(RANGE1.title())
        canvas.ax.set_ylabel("Rp.")
        canvas.ax.set_title("Complete Plot", pad=20)
    
        curData['Expenses']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Expenses', alpha=0.6)
        curData['Revenue']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Revenue', alpha=0.6)
        curData['TOTAL'].cumsum().plot(ax=canvas.ax, label='Budget', alpha=0.6)
    
        canvas.ax.legend()
        # canvas.fig.tight_layout()
        canvas.draw()

        if parent is not None:
            layout = parent.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(parent)
                parent.setLayout(layout)
            layout.addWidget(canvas)

typeMapping = {
    0: "Foods & Drinks",
    1: "Transportation",
    2: "Entertainment", 
    3: "Healthcare",
    4: "Asurance",
    5: "Luxury",
    10: "Fixed Income",
    11: "Passive Income",
    12: "Invest Income",
    13: "Other Income"
}