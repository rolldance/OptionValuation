import numpy as np
from scipy import stats
from math import *
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)

def bsmImpVolatility(C_P, S0, K, T, V, r, q):
    if C_P == 'C':
        par = 1.0
    elif C_P == 'P':
        par = -1.0
    else:
        return ("the value can not be calculatable")

    ITERATION = 1000
    e = 10e-7
    sigma = sqrt(2 * abs((log(float(S0) / K + r * T)) / T))

    for i in range(ITERATION):
        d1 = (log(float(S0) / K) + ((r - q) * 0.5 * sigma ** 2)) * T / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        Vc = par * S0 * exp(-q * T) * stats.norm.cdf(par * d1) - par * K * exp(-r * T) * stats.norm.cdf(par * d2)
        nominator = Vc - V
        vega = S0 * exp(-q * T) * sqrt(T) * stats.norm.pdf(d1)

        if vega == 0:
            return 'NaN'

        if abs(nominator) < e:
            break

        sigma -= nominator / vega

        if i == ITERATION - 1:
            return "NaN"

    return sigma
class bsm_ImpVolatility(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.C_P = QLabel('CallOrPut')
        self.S0 = QLabel('S0')
        self.K = QLabel('K')
        self.T = QLabel('T')
        self.r = QLabel('r')
        self.q = QLabel('q')
        self.V = QLabel('V')
        self.result = QLabel('result')

        self.C_Pcombo = QComboBox(self)
        self.C_Pcombo.addItem("call")
        self.C_Pcombo.addItem("put")
        self.C_Pcombo.activated[str].connect(self.onActivated)

        self.S0ed = QLineEdit()
        self.Ked = QLineEdit()
        self.Ted = QLineEdit()
        self.red = QLineEdit()
        self.qed = QLineEdit()
        self.Ved = QLineEdit()

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
        grid.addWidget(self.q, 3, 0)
        grid.addWidget(self.qed, 3, 1)
        grid.addWidget(self.V, 3, 2)
        grid.addWidget(self.Ved, 3, 3)

        grid.addWidget(btn, 4, 0)
        grid.addWidget(self.result, 4, 1)




        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('bsmImpVol')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S0 = float(self.S0ed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        q = float(self.qed.text())
        V = float(self.Ved.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = bsmImpVolatility(C_P, S0, K, T, V, r, q)
        self.result.setText(str(result))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = bsm_ImpVolatility()
    sys.exit(app.exec_())