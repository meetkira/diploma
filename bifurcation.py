from sympy import symbols, Float, diff, Matrix, solve
import numpy as np
import matplotlib.pyplot as plt

from cardano import cardano
from data import data
from utils import undim

T, c = symbols("T c")


def is_stable(n, t, c, data):
    x, y = symbols('x y')

    diff_1 = data["c_in"] - data["f"] * x + data["g"] * x * y / (data["h"] + y) - data["p"] * x * y
    diff_2 = y * (1 - y) - c * x * y

    diff_1_dx = diff(diff_1, x)
    diff_1_dy = diff(diff_1, y)
    diff_2_dx = diff(diff_2, x)
    diff_2_dy = diff(diff_2, y)

    diff_1_dx_1 = diff_1_dx.subs([(x, n), (y, t)])
    diff_1_dy_1 = diff_1_dy.subs([(x, n), (y, t)])
    diff_2_dx_1 = diff_2_dx.subs([(x, n), (y, t)])

    diff_2_dy_1 = diff_2_dy.subs([(y, t)])
    diff_2_dy_1 = diff_2_dy_1.subs([(x, n)])

    A = Matrix([[diff_1_dx_1, diff_1_dy_1], [diff_2_dx_1, diff_2_dy_1]])
    values = list(A.eigenvals().keys())
    for i in values:
        a = i if isinstance(i, Float) or i == 0 else i.args[0]
        if a > 0:
            return False
    return True



def plot_bif(eq, c_list, data):
    k = (data["alpha"] * data["e"]) / (data["a"]) ** 3
    for i in c_list:
        result = solve(eq.subs([(c, i)]))
        for res in result:
            t = res if isinstance(res, Float) else res.args[0]
            n = (1 - t) / i
            if is_stable(n, t, i, data):
                marker = "_"
                color = "blue"
            else:
                marker = "|"
                color = "red"
            plt.scatter(i/k, t/data["b"], marker=marker, c=color)

    plt.yscale('symlog')
    plt.xlabel("c, cell^-1*day^-1")
    plt.ylabel("T, cell")
    plt.tight_layout()
    # plt.grid()
    plt.show()


c_dict = {
    "mouse": np.arange(1e-8, 4 * 10e-7, 1e-8),
    "patient_1": np.arange(1e-4, 5e-3, 1e-5),
    "patient_2": np.arange(1e-4, 2.5e-3, 1e-5),
}

def plot_all():
    for title, data_ in data.items():
        eq = cardano(need_eq=True)
        undim_data = undim(data_)
        syms = []
        for sym in eq.free_symbols:
            if str(sym) not in "xycT":
                try:
                    syms.append((sym, undim_data[str(sym)]))
                except Exception:
                    raise
        eq = eq.subs(syms)

        plot_bif(eq=eq, c_list=c_dict[title], data=undim_data)


plot_all()
