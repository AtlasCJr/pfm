from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from Functions.chats import getBotAnswer

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter

from scipy.stats import linregress

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
    def __init__(self, parent=None, figsize=(9, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=50)
        super().__init__(self.fig)
        self.setParent(parent)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.updateGeometry()

class enrichedData:
    def __init__(self, old_data: pd.DataFrame, data: pd.DataFrame, figsize: tuple[int, int] = (20, 10)) -> None:
        self.old_data = old_data
        self.data = data
        self.figsize = figsize

    def getLinReg(self):
        data = self.data

        totalYear = self.data['Features'].iloc[-1]['YEAR'] - self.data['Features'].iloc[0]['YEAR'] + 1

        linreg = []
        for y in ['Expenses', 'Revenue']:
            curtype = []
            for x in ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR']:
                cur_data = data.copy()
                cur_data[x] = cur_data['Features'][x]
                cur_data = cur_data.groupby(x, as_index=False)[y].sum()
                cur_data['Cumulative'] = cur_data[y]['TOTAL'].cumsum()

                slope, intercept, r_value, p_value, std_err = linregress(cur_data[x], cur_data['Cumulative'])

                slope /= totalYear

                curtype.append(slope)
            
            linreg.append(curtype)

        curtype = []
        for i in range(5):
            curtype.append(linreg[1][i] - linreg[0][i])
        
        linreg.append(curtype)

        return linreg
        

    def plotAll(self, RANGE1: str, RANGE2: str, displacement: tuple[int, ...], parent):
        if parent.layout() is None:
            layout = QtWidgets.QVBoxLayout(parent)
            parent.setLayout(layout)
        else:
            layout = parent.layout()

        if parent is not None:
            for i in reversed(range(parent.layout().count())):
                widget_to_remove = parent.layout().itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)
                    widget_to_remove.deleteLater()

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
    
        curData['Expenses']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Expenses', alpha=0.6, linewidth=2)
        curData['Revenue']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Revenue', alpha=0.6, linewidth=2)
        curData['TOTAL'].cumsum().plot(ax=canvas.ax, label='Budget', alpha=0.6, linewidth=2)

        if RANGE1 == "YEAR":
            canvas.ax.set_xticks(curData.index)
            canvas.ax.set_xticklabels([int(year) for year in curData.index])

        def format_y(value, tick_number):
            return f'{value / 1e8:.1f}e8'

        canvas.ax.yaxis.set_major_formatter(FuncFormatter(format_y))
    
        canvas.ax.legend()
        canvas.ax.grid(True)
        # canvas.fig.tight_layout()
        canvas.draw()

        if parent is not None:
            layout = parent.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(parent)
                parent.setLayout(layout)
            layout.addWidget(canvas)

    def plotCategory(self, cat: int, parent):
        # Set up the layout for the parent widget
        if parent.layout() is None:
            layout = QtWidgets.QVBoxLayout(parent)
            parent.setLayout(layout)
        else:
            layout = parent.layout()

        # Clear any existing widgets in the layout
        if parent is not None:
            for i in reversed(range(parent.layout().count())):
                widget_to_remove = parent.layout().itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)
                    widget_to_remove.deleteLater()

        # Create a new canvas to draw the plot
        canvas = Canvas(parent, figsize=self.figsize)

        # Define the type categories to be plotted
        all_types = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13]

        # Group by 'TYPE' and sum 'VALUE', ensuring all types are included
        byType = self.old_data.groupby('TYPE')['VALUE'].sum().reset_index()
        byType = byType.set_index('TYPE').reindex(all_types, fill_value=0).reset_index()

        # Mapping 'TYPE' to 'TYPE_LABEL'
        byType['TYPE_LABEL'] = byType['TYPE'].map(typeMapping)

        # Sort the values in descending order
        byType = byType.sort_values("VALUE", ascending=False)

        # Create color mapping based on 'TYPE'
        colors = ["red" if type_val < 10 else "green" for type_val in byType['TYPE']]

        # Plot the bar graph on the canvas axes
        canvas.ax.bar(byType['TYPE_LABEL'], byType['VALUE'], color=colors)

        # Set the labels and title
        canvas.ax.set_xlabel('Type')
        canvas.ax.set_ylabel('Rp.')
        canvas.ax.set_title('Expenses by Type', pad=20)
        canvas.ax.set_xticks(range(len(byType['TYPE_LABEL'])))
        canvas.ax.set_xticklabels(byType['TYPE_LABEL'], rotation=45, ha='right')

        # Add a title text above the plot
        canvas.ax.text(0.5, 1.01, f"All Year", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=15)

        # Show the grid and draw the canvas
        canvas.ax.grid(True)
        canvas.draw()

        # Add the canvas to the parent widget layout
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