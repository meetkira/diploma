import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

from data import data
from utils import undim


class PhasePortrait:

    def __init__(self, data):
        self.data = undim(data)

    def __ode(self, Y, y0, t):
        x, y = Y
        dydt = [self.data["c_in"] - self.data["f"] * x + self.data["g"] * x * y / (self.data["h"] + y) - self.data["p"] * x * y,
                y * (1 - y) - self.data["c"] * x * y]
        return dydt


    def _calcODE(self, args, y0, dy0, ts=10, nt=101):
        y0 = [y0, dy0]
        t = np.linspace(0, ts, nt)
        sol = odeint(self.__ode, y0, t, args)
        return sol


    def drawPhasePortrait(self, args, deltaX=1.0, deltaDX=1.0, startX=0.0, stopX=5.0, startDX=0.0, stopDX=5.0, ts=10, nt=101, xlim=None, ylim=None):
        for y0 in np.arange(startX, stopX, deltaX):
            for dy0 in np.arange(startDX, stopDX, deltaDX):
                sol = self._calcODE(args=args, y0=y0, dy0=dy0, ts=ts, nt=nt)
                plt.plot(sol[:, 0], sol[:, 1], 'b')
        plt.title('Фазовый портрет')
        plt.xlabel('N')
        plt.ylabel('T')
        plt.grid()
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        plt.show()


args =  (1,)

def plot_mouse():
    mouse_portrait = PhasePortrait(data["mouse"])
    # (375;0)
    mouse_portrait.drawPhasePortrait(args=args,deltaX=25, deltaDX=5*10**(-13), startX=100, stopX=1000, startDX=0,
                      stopDX=10*10**(-12), ts=5, nt=301, xlim=[200, 500], ylim=[0, 12 * 10 ** (-12)])
    # (3.7;0.999)
    mouse_portrait.drawPhasePortrait(args=args, deltaX=100, deltaDX=0.1, startX=0, stopX=600, startDX=0,
                      stopDX=2, ts=5, nt=301, xlim=[0, 500], ylim=[0, 2])
    # (648080.0;  0.0991308)
    mouse_portrait.drawPhasePortrait(args=args, deltaX=10**6, deltaDX=0.005, startX=0.5*10**6, stopX=0.2*10**7, startDX=0.025,
                      stopDX=0.3, ts=5, nt=301, xlim=[0, 0.2*10**7], ylim=[0, 0.2])
    # (719395.0; 8.57422*10^(-10))
    mouse_portrait.drawPhasePortrait(args=args, deltaX=10**5, deltaDX=10**(-10), startX=0.2*10**6, stopX=0.2*10**7, startDX=2*10**(-10),
                      stopDX=12*10**(-10), ts=5, nt=301, xlim=[0, 0.2 * 10 ** 7], ylim=[0, 12*10**(-10)])

def plot_patient_1():
    patient_1_portrait = PhasePortrait(data["patient_1"])
    # (0.00461683; 1.0)
    patient_1_portrait.drawPhasePortrait(args=args, deltaX=20, deltaDX=0.5, startX=0, stopX=400, startDX=0,
                      stopDX=10, ts=5, nt=301, xlim=[0, 400], ylim=[0, 6])
    # (375;0)
    patient_1_portrait.drawPhasePortrait(args=args, deltaX=25, deltaDX=5*10**(-13), startX=100, stopX=1000, startDX=0,
                      stopDX=10*10**(-12), ts=5, nt=301, xlim=[200, 500], ylim=[0, 12 * 10 ** (-12)])

def plot_patient_2():
    patient_2_portrait = PhasePortrait(data["patient_2"])
    # (0.00659731;1.0)
    patient_2_portrait.drawPhasePortrait(args=args, deltaX=1, deltaDX=0.2, startX=0, stopX=25, startDX=0,
                      stopDX=6, ts=5, nt=301, xlim=[0, 25], ylim=[0.5, 3])
    # (536;0)
    patient_2_portrait.drawPhasePortrait(args=args, deltaX=25, deltaDX=5*10**(-13), startX=100, stopX=1000, startDX=0,
                      stopDX=10*10**(-12), ts=5, nt=301, xlim=[400, 700], ylim=[0, 12 * 10 ** (-12)])

def plot_all():
    plot_mouse()
    plot_patient_1()
    plot_patient_2()

plot_all()
