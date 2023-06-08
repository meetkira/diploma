from typing import List

import wolframalpha
from sympy import symbols, Matrix, eye, solve, Float

from utils import to_file_and_console


class WolframClient:

    def __init__(self, app_id):
        self.check_client(app_id)

    def client(self):
        return self._client

    def check_client(self, app_id):
        try:
            self._client = wolframalpha.Client(app_id)
            self._client.query("test")
        except Exception:
            raise

    @staticmethod
    def __validate_dots(dot: str) -> float:
        """
        Преобразование точек вида a×10^k к типу float
        """
        dot = dot.replace("^", "**")
        dot = dot.replace("×", "*")
        numbers = dot.split("*")
        dot = float(numbers[0]) * int(numbers[1]) ** int(numbers[-1])
        return dot

    def get_dots(self, system, file):
        """
        Вычисление особоых точек системы при помощи WolframAlphaAPI
        """
        request = f"solve"
        for eq in system.eqs:
            request = request + f" {eq.eq} = 0"
        response = self._client.query(request)
        result = next(response.results).texts
        to_file_result = '\n'.join(result)
        to_file_and_console(file, f"{to_file_result}\n")

        dots = []
        for res in result:
            res_ = res.split()
            try:
                if "^" in res_[2] or "×" in res_[2]:
                    x = self.__validate_dots(res_[2])
                else:
                    x = float(res_[2])
                if "^" in res_[-1] or "×" in res_[-1]:
                    y = self.__validate_dots(res_[-1])
                else:
                    y = float(res_[-1])
                dot = Dot(x=x, y=y, file=file, lin_eqs=system.lin_eqs)
                dots.append(dot)
            except Exception as e:
                print(e)

        return dots


class Dot:
    def __init__(self, x, y, file, lin_eqs):
        self.x = x
        self.y = y
        self.lin_eqs = lin_eqs
        self.file = file
        self.__s = symbols("s")

    def _set_num_lin_eqs(self):
        lin_eqs = []
        to_file_and_console(self.file, f"Точка для расчета: ({self.x};{self.y})")
        for item in self.lin_eqs:
            num_eq = Equation(title=item.title, eq=item.eq.subs([(Equation.x, self.x), (Equation.y, self.y)]))
            lin_eqs.append(num_eq)
            to_file_and_console(self.file, num_eq)
        to_file_and_console(self.file, "")
        self.num_lin_eqs = lin_eqs

    def _set_matrix(self):
        self._A = Matrix(
            [[self.num_lin_eqs[0].eq, self.num_lin_eqs[2].eq], [self.num_lin_eqs[1].eq, self.num_lin_eqs[3].eq]])
        to_file_and_console(self.file, "A = ")
        to_file_and_console(self.file, self._A, special_out=True)
        to_file_and_console(self.file, "")

    def _set_HP(self):
        HP = self.__s * eye(2) - self._A
        to_file_and_console(self.file, "sE - A = ")
        to_file_and_console(self.file, HP, special_out=True)
        to_file_and_console(self.file, "")

        self._HP = HP.det()
        to_file_and_console(self.file, f"Характеристический полином\ndet(sE - A) = {self._HP} = 0\n")

    def _set_roots(self):
        self._roots = solve(self._HP, self.__s)
        to_file_and_console(self.file, f"Корни характеристического полинома:\n{self._roots}\n")

    def _set_type(self):
        """
        Определение типа особой точки
        """
        if not self._roots:
            raise Exception("Ошибка при определении типа особой точки")
        if isinstance(self._roots[0], Float):
            if self._roots[0] * self._roots[1] < 0:
                self._type = "Седло"
            elif self._roots[0] > 0:
                self._type = "Неустойчивый узел"
            else:
                self._type = "Устойчивый узел"
        else:
            if self._roots[0].args[0] == 0 and self._roots[1].args[0] == 0:
                self._type = "Центр"
            elif self._roots[0].args[0] > 0.0 and self._roots[1].args[0] > 0.0:
                self._type = "Неустойчивый фокус"
            else:
                self._type = "Устойчивый фокус"

    def get_type(self):
        self._set_num_lin_eqs()
        self._set_matrix()
        self._set_HP()
        self._set_roots()
        self._set_type()
        to_file_and_console(self.file, f"Тип особой точки ({self.x};{self.y}) - {self._type}\n\n")


class Equation:
    x, y = symbols("x, y")

    def __init__(self, title, eq):
        self.title = title
        self.eq = eq

    def __str__(self):
        return f"{self.title} = {self.eq}"


class System:
    x, y = symbols("x, y")

    def __init__(self, eqs: List[Equation], lin_eqs: List[Equation]):
        self.eqs = eqs
        self.lin_eqs = lin_eqs

    @property
    def symbols(self):
        return self._symbols

    def set_symbols(self):
        self._symbols = self.eqs[0].eq.free_symbols
        for eq in self.eqs:
            self._symbols = self._symbols.union(eq.eq.free_symbols)
        self._symbols = self._symbols.difference({self.x, self.y})


class GeneralSystem(System):
    def __init__(self, eqs: List[Equation], lin_eqs: List[Equation], client: WolframClient):
        self.client = client
        super().__init__(eqs=eqs, lin_eqs=lin_eqs)
