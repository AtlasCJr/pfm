from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

from Functions.chat import getBotAnswer
from Functions.dicts import *

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter

from scipy.stats import linregress

import numpy as np
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

class botChat(QThread):
    resultReady = pyqtSignal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        bot_answer = getBotAnswer(self.question)
        self.resultReady.emit(bot_answer)

class Canvas(FigureCanvas):
    def __init__(self, figsize, parent=None):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=60)
        super().__init__(self.fig)
        self.setParent(parent)

class enrichedData:
    def __init__(self, old_data: pd.DataFrame, data: pd.DataFrame, figsize: tuple[int, int] = (15, 5)) -> None:
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

        canvas = Canvas(figsize=self.figsize, parent=parent)
        
        if RANGE1 != "YEAR":
            last_data = self.data['Features', RANGE2].iloc[-1] - displacement
            curData = self.data[self.data['Features', RANGE2] == last_data]
            curData = curData.groupby(self.data['Features'][RANGE1]).sum()

            canvas.ax.text(0.5, 1.01, f"{RANGE2.title()} {last_data}", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=15)
        else:
            curData = self.data.groupby(self.data['Features']['YEAR']).sum()
            last_data = curData.index[-1]

            canvas.ax.text(0.5, 1.04, f"All Year", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=10)

        canvas.ax.set_xlabel('')
        canvas.ax.set_title("Complete Plot", pad=20)
    
        curData['Expenses']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Expenses', alpha=0.6, linewidth=2)
        curData['Revenue']['TOTAL'].cumsum().plot(ax=canvas.ax, label='Cumulative Revenue', alpha=0.6, linewidth=2)
        curData['TOTAL'].cumsum().plot(ax=canvas.ax, label='Budget', alpha=0.6, linewidth=2)

        if RANGE1 == "YEAR":
            canvas.ax.set_xticks(curData.index)
            canvas.ax.set_xticklabels([int(year) for year in curData.index])
    
        canvas.ax.legend()

        max_value = max(
            curData['TOTAL'].cumsum().max(),
            curData['Expenses']['TOTAL'].cumsum().max(),
            curData['Revenue']['TOTAL'].cumsum().max()
        )

        power = np.floor(np.log10(max_value)).astype(int)

        yticks_values = np.arange(0, max_value + 10**power, 10**power / 4)
        yticks_labels = [f'{tick / 10**power:.1f}' for tick in yticks_values]

        canvas.ax.set_yticks(yticks_values)
        canvas.ax.set_yticklabels(yticks_labels)

        canvas.ax.set_ylabel(f"{powerMapping.get(power, '')} Rp.")

        canvas.ax.grid(True)
        canvas.fig.tight_layout()


        canvas.draw()

        if parent is not None:
            layout = parent.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(parent)
                parent.setLayout(layout)
            layout.addWidget(canvas)

        exported_data = []
        for year in curData.index:
            exported_data.append([
                curData[('Expenses', 'TOTAL')].loc[year],
                curData[('Revenue', 'TOTAL')].loc[year],
                curData[('Revenue', 'TOTAL')].loc[year] - curData[('Expenses', 'TOTAL')].loc[year]
            ])

        return exported_data, curData.index[0], len(curData.index)

    def plotCategory(self, parent):
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

        canvas = Canvas(figsize=self.figsize, parent=parent)

        all_types = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13]

        byType = self.old_data.groupby('TYPE')['VALUE'].sum().reset_index()
        byType = byType.set_index('TYPE').reindex(all_types, fill_value=0).reset_index()

        byType['TYPE_LABEL'] = byType['TYPE'].map(typeMapping)

        byType = byType.sort_values("VALUE", ascending=False)

        colors = ["red" if type_val < 10 else "green" for type_val in byType['TYPE']]

        canvas.ax.bar(byType['TYPE_LABEL'], byType['VALUE'], color=colors)

        canvas.ax.set_xlabel('')
        canvas.ax.set_ylabel('Rp.')
        canvas.ax.set_title('Expenses by Type', pad=20)
        canvas.ax.set_xticks(range(len(byType['TYPE_LABEL'])))
        canvas.ax.set_xticklabels(byType['TYPE_LABEL'], rotation=45, ha='right')

        max_value = byType['VALUE'].max()
        power = np.floor(np.log10(max_value)).astype(int)
        
        yticks_values = np.arange(0, max_value + 10**power, 10**power / 4)

        yticks_labels = [f'{tick / 10**power:.1f}' for tick in yticks_values]

        canvas.ax.set_yticks(yticks_values) 
        canvas.ax.set_yticklabels(yticks_labels)

        canvas.ax.set_ylabel(f"{powerMapping.get(power, '')} Rp.")

        canvas.ax.text(0.5, 1.04, f"All Year", ha='center', va='center', transform=canvas.ax.transAxes, fontsize=10)
        canvas.ax.grid(True)
        canvas.fig.tight_layout()
        canvas.draw()

        if parent is not None:
            layout = parent.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(parent)
                parent.setLayout(layout)
            layout.addWidget(canvas)

        exported_data = []
        for i in byType.index:
            exported_data.append([
                byType['TYPE_LABEL'][i], 
                byType['VALUE'].loc[i]
            ])

        return exported_data

    def plotTimeCycle(self, x: int, parent):
        if x < 0 or x > 4:
            return

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

        canvas = Canvas(figsize=self.figsize, parent=parent)

        time_cycle = ["DoW", "WoM", "MONTH", "QUARTER", "YEAR"][x]
        time_dict = [dayMapping, weekMapping, monthMapping, quarterMapping, None][x]
        title = ["Day", "Week", "Month", "Quarter", "Year"][x]

        cur_data = self.data.copy()
        cur_data[time_cycle] = cur_data['Features'][time_cycle]

        if time_cycle == "WoM":
            cur_data[time_cycle] = cur_data[time_cycle].replace(6, 5)

        cur_data['ET'] = cur_data[('Expenses', 'TOTAL')]
        cur_data['RT'] = cur_data[('Revenue', 'TOTAL')]
        cur_data = cur_data.sort_index(axis=1)
        cur_data = cur_data.drop(columns=['Features'])

        cur_data = cur_data.groupby(time_cycle, as_index=False).sum()

        # Comment-able
        # if ('Expenses', '5') in cur_data.columns:
        #     cur_data.loc[:, ('Expenses', 'TOTAL')] = cur_data[('Expenses', 'TOTAL')] - cur_data[('Expenses', '5')]

        indices = np.arange(len(cur_data))
        bar_width = 0.35

        canvas.ax.bar(indices, cur_data[('Expenses', 'TOTAL')], width=bar_width, label='Expenses')
        canvas.ax.bar(indices + bar_width, cur_data[('Revenue', 'TOTAL')], width=bar_width, label='Revenue')

        if time_cycle != "YEAR":
            cur_data['LABEL'] = cur_data[time_cycle].map(time_dict).fillna("Unknown")
        else:
            cur_data['LABEL'] = cur_data[time_cycle].astype(str)

        canvas.ax.set_xlabel('')
        canvas.ax.set_xticks(indices + bar_width / 2)
        if time_cycle == "MONTH":
            canvas.ax.set_xticklabels(cur_data['LABEL'], rotation=45, ha='right')
        else:
            canvas.ax.set_xticklabels(cur_data['LABEL'])
        canvas.ax.set_ylabel('Rp.')
        canvas.ax.set_title(f'{title} Distribution', pad=20)

        canvas.ax.grid(True)
        canvas.ax.legend()

        max_value = max(
            cur_data[('Expenses', 'TOTAL')].cumsum().max(),
            cur_data[('Revenue', 'TOTAL')].cumsum().max(),
        )

        power = np.floor(np.log10(max_value)).astype(int)
        yticks_values = np.arange(0, max_value/1.5, 10**power/4)
        yticks_labels = [f'{tick / 10**power:.1f}' for tick in yticks_values]

        canvas.ax.set_yticks(yticks_values) 
        canvas.ax.set_yticklabels(yticks_labels)
        canvas.ax.set_ylabel(f"{powerMapping.get(power, '')} Rp.")

        canvas.fig.tight_layout()
        canvas.draw()

        layout.addWidget(canvas)

        exported_data = []
        for i in cur_data.index:
            exported_data.append([
                cur_data['ET'].loc[i],
                cur_data['RT'].loc[i]
            ])

        if time_cycle == "YEAR":
            start = cur_data['YEAR'].loc[0]
        else:
            start = None

        return title, exported_data, time_dict, start