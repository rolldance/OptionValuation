import numpy as np
from math import *
from scipy import stats
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)


def cffBasketOption(C_P, S01, S02, K, T, r, sigma1, sigma2, cov):
    if C_P == 'C':
        par = 1.0
    elif C_P == 'P':
        par = -1.0
    else:
        return ("the value can not be calculatable")

    B0 = sqrt(S01 * S02)
    Bsigma = 0.5 * sqrt(sigma1 ** 2 + sigma2 ** 2 + 2 * sigma1 * sigma2 * cov)
    Bu = r - (sigma1 ** 2 + sigma2 ** 2) / (2 * 2) + 0.5 * Bsigma ** 2
    d1_x_nominator = log(float(B0) / K) + (Bu + 0.5 * Bsigma ** 2) * T
    d1_x = d1_x_nominator / (Bsigma * sqrt(T))
    d2_x = d1_x - Bsigma * sqrt(T)

    VhT = par * B0 * exp(Bu * T) * stats.norm.cdf(par * d1_x) - par * K * stats.norm.cdf(par * d2_x)
    VBcff = exp(-r * T) * VhT

    return VBcff

class cff_BasketOption(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.C_P = QLabel('CallOrPut')
        self.S01 = QLabel('S01')
        self.S02 = QLabel('S02')
        self.K = QLabel('K')
        self.T = QLabel('T')
        self.r = QLabel('r')
        self.sigma1 = QLabel('sigma1')
        self.sigma2 = QLabel('sigma2')
        self.cov = QLabel('cov')
        self.result = QLabel('result')

        self.C_Pcombo = QComboBox(self)
        self.C_Pcombo.addItem("call")
        self.C_Pcombo.addItem("put")
        self.C_Pcombo.activated[str].connect(self.onActivated)

        self.S01ed = QLineEdit()
        self.S02ed = QLineEdit()
        self.Ked = QLineEdit()
        self.Ted = QLineEdit()
        self.red = QLineEdit()
        self.sigma1ed = QLineEdit()
        self.sigma2ed = QLineEdit()
        self.coved = QLineEdit()

        btn = QPushButton("calculate")
        btn.clicked.connect(self.buttonClicked)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.C_P, 0, 0)
        grid.addWidget(self.C_Pcombo, 0, 1)
        grid.addWidget(self.S01, 1, 0)
        grid.addWidget(self.S01ed, 1, 1)
        grid.addWidget(self.S02, 1, 2)
        grid.addWidget(self.S02ed, 1, 3)
        grid.addWidget(self.K, 2, 0)
        grid.addWidget(self.Ked, 2, 1)
        grid.addWidget(self.T, 2, 2)
        grid.addWidget(self.Ted, 2, 3)
        grid.addWidget(self.r, 3, 0)
        grid.addWidget(self.red, 3, 1)
        grid.addWidget(self.sigma1, 3, 2)
        grid.addWidget(self.sigma1ed, 3, 3)
        grid.addWidget(self.sigma2, 4, 0)
        grid.addWidget(self.sigma2ed, 4, 1)
        grid.addWidget(self.cov, 4, 2)
        grid.addWidget(self.coved, 4, 3)

        grid.addWidget(btn, 5, 0)
        grid.addWidget(self.result, 5, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('cffBasketOption')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S01 = float(self.S01ed.text())
        S02 = float(self.S02ed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        sigma1 = float(self.sigma1ed.text())
        sigma2 = float(self.sigma2ed.text())
        cov = float(self.coved.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = cffBasketOption(C_P, S01, S02, K, T, r, sigma1, sigma2, cov)
        self.result.setText(str(result))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cff_BasketOption()
    sys.exit(app.exec_())


