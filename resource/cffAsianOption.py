from math import *
import numpy as np
from scipy import stats
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)

def cffAsianOption(C_P, S0, K, T, r, sigma, M):
    if C_P == 'C':
        par = 1.0
    elif C_P == 'P':
        par = -1.0
    else:
        return ("the value can not be calculatable")

    np.random.seed(2000)
    sigma_x = sigma * sqrt(float((M + 1) * (2 * M + 1)) / (6 * M ** 2))
    r_x = float((r - 0.5 * sigma ** 2) * (M + 1)) / (2 * M) + 0.5 * sigma_x ** 2

    d1 = (log(float(S0) / K) + (r_x + 0.5 * sigma_x ** 2) * T) / (sigma_x * sqrt(T))
    d2 = d1 - sigma_x * sqrt(T)
    S_cff = par * S0 * exp(r_x * T) * stats.norm.cdf(par * d1)
    K_cff = par * K * stats.norm.cdf(par * d2)
    Vcff = exp(-r * T) * (S_cff - K_cff)

    return Vcff

class cff_AsianOption(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.C_P = QLabel('CallOrPut')
        self.S0 = QLabel('S0')
        self.K = QLabel('K')
        self.T = QLabel('T')
        self.r = QLabel('r')
        self.sigma = QLabel('sigma')
        self.M = QLabel('M')
        self.result = QLabel('result')

        self.C_Pcombo = QComboBox(self)
        self.C_Pcombo.addItem("call")
        self.C_Pcombo.addItem("put")
        self.C_Pcombo.activated[str].connect(self.onActivated)

        self.S0ed = QLineEdit()
        self.Ked = QLineEdit()
        self.Ted = QLineEdit()
        self.red = QLineEdit()
        self.sigmaed = QLineEdit()
        self.Med = QLineEdit()

        btn = QPushButton("calculate")
        btn.clicked.connect(self.buttonClicked)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.C_P, 0, 0)
        grid.addWidget(self.C_Pcombo, 0, 1)
        grid.addWidget(self.S0, 1, 0)
        grid.addWidget(self.S0ed, 1, 1)
        grid.addWidget(self.K, 1, 2)
        grid.addWidget(self.Ked, 1, 3)
        grid.addWidget(self.T, 2, 0)
        grid.addWidget(self.Ted, 2, 1)
        grid.addWidget(self.r, 2, 2)
        grid.addWidget(self.red, 2, 3)
        grid.addWidget(self.sigma, 3, 0)
        grid.addWidget(self.sigmaed, 3, 1)
        grid.addWidget(self.M, 3, 2)
        grid.addWidget(self.Med, 3, 3)

        grid.addWidget(btn, 4, 0)
        grid.addWidget(self.result, 4, 1)




        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('cffAsianOption')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S0 = float(self.S0ed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        sigma = float(self.sigmaed.text())
        M = float(self.Med.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = cffAsianOption(C_P, S0, K, T, r, sigma, M)
        self.result.setText(str(result))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cff_AsianOption()
    sys.exit(app.exec_())
