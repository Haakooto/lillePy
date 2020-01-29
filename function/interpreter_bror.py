# import numpy as np
import numbers


def listed_nest_remover(l):
    nested_list_dummy = []

    def list_nested_remover_2(l):
        for i in l:
            if isinstance(i, list):
                list_nested_remover_2(i)
            else:
                nested_list_dummy.append(i)

    list_nested_remover_2(l)
    return nested_list_dummy


def index_symbols(string, *symbol):
    symbls = []
    # first find possible symbol to the left:
    lsymb = None
    for i, symb in enumerate(string):
        if symb in list(symbol):
            symbls.append(i)
    return symbls


class Variable:
    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return str(self.var_name)

    def __call__(self, *args):
        print("__call__ in variable")
        assert len(args) == 1
        arg = args[0]
        print(arg)
        return self


if __name__ == "__main__":
    x = Variable("x")
    a = sub(1, 1)
    print(a(2))
