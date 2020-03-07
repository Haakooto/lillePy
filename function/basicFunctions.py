import numpy as np
import sys
from numbers import Number

from .Variable import Variable
from .parents import parentFunction, parentOperator


class div(parentFunction):
    arglen = 2

    def call(self, *args):
        return args[0][0] / args[0][1]

    def string(self):
        numer = self.structure[0]
        denom = self.structure[1]
        res = ""

        if " " in str(numer):
            res += f"({str(numer)})"
        else:
            res += str(numer)
        if " " in str(denom):
            res += f"/({str(denom)})"
        else:
            res += f"/{str(denom)}"

        return res


class pow(parentFunction):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        return args[0] ** args[1]

    def string(self):
        arg1, arg2 = self.structure
        if " " in str(arg2):
            return f"{str(arg1)}^({str(arg2)})"
        else:
            return f"{str(arg1)}^{str(arg2)}"


class sqrt(parentFunction):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        return args[0] ** (1 / 2)

    def string(self):
        return f"sqrt({str(self.structure[0])})"


class cos(parentFunction):
    arglen = 1
    func_name = "cos"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "cos takes 1 argument a -> cos(a)"
        return np.cos(arg[0])

    def string(self):
        return f"cos({str(self.structure[0])})"


class sin(parentFunction):
    arglen = 1
    arg_example = "sin(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "sin takes 1 argument a -> sin(a)"
        return np.sin(arg[0])

    def string(self):
        return f"sin({str(self.structure[0])})"


class ln(parentFunction):
    arglen = 1
    arg_example = "ln(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "ln takes 1 argument a -> ln(a)"
        return np.log(arg[0])

    def string(self):
        return f"ln({str(self.structure[0])})"


if __name__ == "__main__":
    x = Variable("x")
    a = add(1, 2)
    k = mul(1, 2, x, x, sin(x), sin(x))
    print(mul(2, sin(x)))
