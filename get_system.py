import os.path
from typing import TextIO

import wolframalpha
from sympy import symbols, diff

from classes.system import WolframClient
from classes.system import Equation, System, GeneralSystem
from utils import to_file_and_console


def connect_to_wolfram():
    # AppID = "U7322V-UV2UEAAG42"
    # https://products.wolframalpha.com/simple-api/documentation
    AppID = input("Введите ID Вашего приложения в WolframAlpha: ")
    try:
        client = wolframalpha.Client(AppID)
        client.query("test")
    except Exception:
        raise
    return client


def get_general_view(file: TextIO, client: WolframClient):
    """
    Вывод уравнений в общем виде и их линеаризация
    """
    to_file_and_console(file, "Уравнения в общем виде:")
    t, x, y, s, beta, f, g, h, p, c = symbols('t x y s beta f g h p c')

    diff_1 = 1 / beta - f * x + g * x * y / (h + y) - p * x * y
    diff_2 = y * (1 - y) - c * x * y

    eqs = [Equation(title="dx/dt", eq=diff_1), Equation(title="dy/dt", eq=diff_2)]
    for eq in eqs:
        to_file_and_console(file, eq)
    to_file_and_console(file, "")

    to_file_and_console(file, "Линеаризуем: ")
    lin_eqs = [Equation(title="dv1/dx", eq=diff(diff_1, x)),
               Equation(title="dv1/dy", eq=diff(diff_1, y)),
               Equation(title="dv2/dx", eq=diff(diff_2, x)),
               Equation(title="dv2/dy", eq=diff(diff_2, y))]

    for eq in lin_eqs:
        to_file_and_console(file, eq)
    to_file_and_console(file, "")

    system = GeneralSystem(eqs=eqs, lin_eqs=lin_eqs, client=client)
    return system


def get_system(path):
    # AppID = "U7322V-UV2UEAAG42"
    # https://products.wolframalpha.com/simple-api/documentation
    AppID = input("Введите ID Вашего приложения в WolframAlpha: ")
    client = WolframClient(app_id=AppID)
    with open(f'{path}/general.txt', 'w', encoding="utf-8") as file:
        to_file_and_console(file, "Пусть N = x, T = y\n")
        system = get_general_view(file, client)
    return system
