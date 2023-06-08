from contextlib import redirect_stdout

from typing import Dict

import latex2mathml.converter
from sympy import latex, pprint


def sym_to_word(eq):
    latex_input = latex(eq)
    mathml_output = latex2mathml.converter.convert(latex_input)
    return mathml_output


def to_file_and_console(file, data, special_out=False):
    if not special_out:
        print(data)
        file.write(f"{data}\n")
    else:
        pprint(data, use_unicode=True)
        with redirect_stdout(file):
            pprint(data, wrap_line=False)


def undim(data: Dict):
    data["c"] = (data["c"] * data["alpha"] * data["e"]) / (data["a"]) ** 3
    data["f"] = (data["f"]) / (data["a"])
    data["g"] = (data["g"]) / (data["a"])
    data["h"] = data["h"] * (data["b"]) ** 2
    data["p"] = (data["p"]) / (data["a"] * data["b"])
    data["beta"] = (data["beta"]) / (data["a"])
    data["c_in"] = 1 / data["beta"]

    return data
