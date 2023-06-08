from classes.system import System, Equation
from utils import undim, to_file_and_console

class Object:
    def __init__(self, name, data, system, path):
        print(f"{name.title()}")
        self.name = name
        self.data = undim(data)
        self.system = system
        self.file = open(f"{path}\\{name}.txt", "w", encoding="utf-8")

    def __del__(self):
        self.file.close()

    def _set_system_values_list(self):
        self.system.set_symbols()
        self.values_list = []
        for value in self.system.symbols:
            try:
                self.values_list.append((value, self.data[str(value)]))
            except Exception:
                continue

    def _get_eqs(self):
        eqs = []
        to_file_and_console(self.file, f"Система уравнений для {self.name}: ")
        for item in self.system.eqs:
            num_eq = Equation(title=item.title, eq=item.eq.subs(self.values_list))
            eqs.append(num_eq)
            to_file_and_console(self.file, num_eq)
        to_file_and_console(self.file, "")
        return eqs

    def _get_lin_eqs(self):
        lin_eqs = []
        to_file_and_console(self.file, "Линеаризуем: ")
        for item in self.system.lin_eqs:
            num_eq = Equation(title=item.title, eq=item.eq.subs(self.values_list))
            lin_eqs.append(num_eq)
            to_file_and_console(self.file, num_eq)
        to_file_and_console(self.file, "")
        return lin_eqs


    def _set_num_system(self):
        eqs = self._get_eqs()
        lin_eqs = self._get_lin_eqs()
        self.num_system = System(eqs=eqs, lin_eqs=lin_eqs)

    def _set_dots(self):
        self.dots = self.system.client.get_dots(file=self.file, system=self.num_system)

        for dot in self.dots:
            dot.get_type()

    def solve(self):
        self._set_system_values_list()
        self._set_num_system()
        self._set_dots()
