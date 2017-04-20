import numpy as np
from math import *
from scipy import stats
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)

def bsmEuroOption(C_P, S, K, T, r, sigma):
    if C_P == 'C':
        par = 1.0
    elif C_P == 'P':
        par = -1.0
    else:
        return ("the value can not be calculatable")

    d1 = (log(float(S) / K) + (r * 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    Vo = par * S * stats.norm.cdf(par * d1) - par * K * exp(-r * T) * stats.norm.cdf(par * d2)

    return Vo
class bsm_EuroOption(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.C_P = QLabel('CallOrPut')
        self.S = QLabel('S')
        self.K = QLabel('K')
        self.T = QLabel('T')
        self.r = QLabel('r')
        self.sigma = QLabel('sigma')
        self.result = QLabel('result')

        self.C_Pcombo = QComboBox(self)
        self.C_Pcombo.addItem("call")
        self.C_Pcombo.addItem("put")
        self.C_Pcombo.activated[str].connect(self.onActivated)

        self.Sed = QLineEdit()
        self.Ked = QLineEdit()
        self.Ted = QLineEdit()
        self.red = QLineEdit()
        self.sigmaed = QLineEdit()

        btn = QPushButton("calculate")
        btn.clicked.connect(self.buttonClicked)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.C_P, 0, 0)
        grid.addWidget(self.C_Pcombo, 0, 1)
        grid.addWidget(self.S, 1, 0)
        grid.addWidget(self.Sed, 1, 1)
        grid.addWidget(self.K, 1, 2)
        grid.addWidget(self.Ked, 1, 3)
        grid.addWidget(self.T, 2, 0)
        grid.addWidget(self.Ted, 2, 1)
        grid.addWidget(self.r, 2, 2)
        grid.addWidget(self.red, 2, 3)
        grid.addWidget(self.sigma, 3, 0)
        grid.addWidget(self.sigmaed, 3, 1)

        grid.addWidget(btn, 4, 0)
        grid.addWidget(self.result, 4, 1)




        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('bsmEuroOption')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S = float(self.Sed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        sigma = float(self.sigmaed.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = bsmEuroOption(C_P, S, K, T, r, sigma)
        self.result.setText(str(result))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = bsm_EuroOption()
    sys.exit(app.exec_())
