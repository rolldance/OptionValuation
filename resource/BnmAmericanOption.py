from math import *
import numpy as np
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)


def BinomialTree(type, S0, K, r, sigma, T, N, american="false"):
    # calculate delta T
    deltaT = float(T) / N
    u = exp(sigma * sqrt(deltaT))
    d = 1.0 / u

    fs = np.asarray([0.0 for i in range(N + 1)])

    # stock tree for calculation of expiration values
    fs2 = np.asarray([(S0 * u ** j * d ** (N - j)) for j in range(N + 1)
                      ])
    # strike tree for the stock tree
    fs3 = np.asarray([float(K) for i in range(N + 1)])

    a = exp(r * deltaT)
    p = (a - d) / (u - d)
    oneMinusP = 1.0 - p

    # compute the leaves
    if type == "C":
        fs[:] = np.maximum(fs2 - fs3, 0.0)
    else:
        fs[:] = np.maximum(fs3 - fs2, 0.0)

    # calculate backward option price
    for i in range(N - 1, -1, -1):
        fs[:-1] = np.exp(-r * deltaT) * (p * fs[1:] + oneMinusP * fs[:-1])
        fs2[:] = fs2[:] * u
        if american == 'True':
            if type == "C":
                fs[:] = np.maximum(fs[:], fs2[:] - fs3[:])
            else:
                fs[:] = np.maximum(fs[:], fs3[:] - fs2[:])

    return fs[0]

class bnm_AmericanOption(QWidget):
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
        self.N = QLabel('N')
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
        self.Ned = QLineEdit()

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
        grid.addWidget(self.N, 3, 2)
        grid.addWidget(self.Ned, 3, 3)

        grid.addWidget(btn, 4, 0)
        grid.addWidget(self.result, 4, 1)




        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('BnmAmericanOption')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S0 = float(self.S0ed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        sigma = float(self.sigmaed.text())
        N = int(self.Ned.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = BinomialTree(C_P, S0, K, r, sigma, T, N)
        self.result.setText(str(result))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = bnm_AmericanOption()
    sys.exit(app.exec_())

