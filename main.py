from classes.object import Object
from data import data
from get_system import get_system

if __name__ == "__main__":
    path = "results"
    system = get_system(path)
    for name, data_ in data.items():
        item = Object(name=name, data=data_, system=system, path=path)
        item.solve()
