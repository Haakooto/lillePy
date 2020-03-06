import numpy as np
import sys
from numbers import Number as number
from .parentFunction import parentFunction
from .Variable import Variable


class cos(parentFunction):
    arglen = 1
    arg_example = "cos(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "cos takes 1 argument a -> cos(a)"
        return np.cos(arg[0])

    def string(self, string_arg):
        return f"cos({string_arg})"


class sin(parentFunction):
    arglen = 1
    arg_example = "sin(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "sin takes 1 argument a -> sin(a)"
        return np.sin(arg[0])

    def string(self, string_arg):
        return f"sin({string_arg})"


class ln(parentFunction):
    arglen = 1
    arg_example = "ln(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "ln takes 1 argument a -> ln(a)"
        return np.log(arg[0])

    def string(self, string_arg):
        return f"ln({string_arg})"


if __name__ == "__main__":
    x = Variable("x")
    a = add(1, 2)
    k = mul(1, 2, x, x, sin(x), sin(x))
    print(mul(2, sin(x)))
