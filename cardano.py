from sympy import symbols, sqrt, Eq
from utils import sym_to_word, to_file_and_console

def cardano(need_eq: bool = False):
    y, beta, b, p, g, f, h, c = symbols("y beta b p g f h c")
    A, B, C, D, n, m, Delta, u, v, y_0, T_0, N_0 = symbols("A B C D n m Delta u v y_0 T_0 N_0")
    T = symbols("T")

    A_ = beta * p
    B_ = beta * (f - g - p + p * h) / A_
    C_ = (c - f * beta + f * beta * h + beta * g - p * beta * h) / A_
    D_ = h * (c - f * beta) / A_
    A_ /= A_
    if need_eq:
        return (A_ * T ** 3 + B_ * T ** 2 + C_ * T + D_) * T

    m_ = C_ - (1. / 3.) * B_ ** 2
    n_ = D_ + (2. / 27.) * B_ ** 3 - (1. / 3.) * B_ * C_

    Delta_ = -27 * n_ ** 2 - 4 * m_ ** 3

    u_ = -n_ / 2 + sqrt(-Delta_ / 108)
    v_ = -n_ / 2 - sqrt(-Delta_ / 108)

    y_0_ = (u_) ** (1. / 3.) + (v_) ** (1. / 3.)

    T_0_ = y_0 - 0.33 * B_
    N_0_ = (1 - T_0) / c

    with open("results/cardano.txt", "w") as file:
        for item in [(A, A_), (B, B_), (C, C_), (D, D_), (m, m_), (n, n_), (Delta, Delta_), (u, u_), (v, v_), (y_0, y_0_),
                     (T_0, T_0_), (N_0, N_0_)]:
            to_file_and_console(file, f"{item[0]} = ")
            to_file_and_console(file, sym_to_word(Eq(item[0], item[1])))


cardano()
