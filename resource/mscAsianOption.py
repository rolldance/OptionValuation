from math import *
import numpy as np
from scipy import stats
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QMainWindow, QComboBox)


def mscAsianOption(C_P, S0, K, T, r, sigma, M, I):
    if C_P == 'C':
        par = 1.0
    elif C_P == 'P':
        par = -1.0
    else:
        return ("the value can not be calculatable")

    dt = T / M
    np.random.seed(10000)
    S = np.zeros((M + 1, I))
    ArithSum = np.zeros((1, I))
    GeoSum = np.ones((1, I))
    S[0] = S0
    sigma_x = sigma * sqrt(float((M + 1) * (2 * M + 1)) / (6 * M ** 2))
    r_x = float((r - 0.5 * sigma ** 2) * (M + 1)) / (2 * M) + 0.5 * sigma_x ** 2

    d1 = (log(float(S0) / K) + (r_x + 0.5 * sigma_x ** 2) * T) / (sigma_x * sqrt(T))
    d2 = d1 - sigma_x * sqrt(T)
    S_geoc = par * S0 * exp(r_x * T) * stats.norm.cdf(par * d1)
    K_geoc = par * K * stats.norm.cdf(par * d2)
    Vgeoc = exp(-r * T) * (S_geoc - K_geoc)

    for t in range(1, M + 1):
        z = np.random.standard_normal(I)
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
                                 + sigma * sqrt(dt) * z)

    for i in range(1, M, 2):
        ArithSum += S[i] + S[i + 1]  # ts:time series
        GeoSum *= S[i] * S[i + 1]

    X = np.maximum(par * ArithSum / M - par * K, 0.0)
    Y = np.maximum(par * np.power(GeoSum, 1.0 / M) - par * K, 0.0)
    theta = np.cov(X, Y)[0][1] / np.var(Y)
    D = exp(-r * T)
    Varith = D * np.mean(X)
    Vgeo = D * np.mean(Y)

    # V = Varith+theta*(Vgeoc - Vgeo)
    Varray = D * X + theta * (Vgeoc - D * Y)
    Vmean = np.mean(Varray)
    Vstd = np.std(Varray)
    Vconf = [Vmean - 1.96 * Vstd / sqrt(I), Vmean + 1.96 * Vstd / sqrt(I)]
    return Vmean, Vconf, Varith, Vgeo

class msc_AsianOption(QWidget):
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
        self.I = QLabel('I')
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
        self.Ied = QLineEdit()

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
        grid.addWidget(self.I, 4, 0)
        grid.addWidget(self.Ied, 4, 1)

        grid.addWidget(btn, 5, 0)
        grid.addWidget(self.result, 5, 1)




        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('mcsAsianOption')
        self.show()

    def buttonClicked(self):
        cp = self.C_P.text()
        S0 = float(self.S0ed.text())
        K = float(self.Ked.text())
        T = float(self.Ted.text())
        r = float(self.red.text())
        sigma = float(self.sigmaed.text())
        M = int(self.Med.text())
        I = int(self.Ied.text())
        if cp == 'put':
            C_P = 'P'
        else:
            C_P = 'C'
        result = mscAsianOption(C_P, S0, K, T, r, sigma, M, I)
        self.result.setText('result: '+str(result[0]) +'\n'+ 'confidence Interval: ' + str(result[1])+
        '\n'+'classic MonteCarlo: '+ str(result[2]) +'\n'+'geographic simulation: '+ str(result[3]))

    def onActivated(self, text):
        self.C_P.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = msc_AsianOption()
    sys.exit(app.exec_())
