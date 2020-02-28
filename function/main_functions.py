import numpy as np
import sys
from numbers import Number as number
from parentFunction import parentFunction


class Variable:
    def __init__(self, name=""):
        try:
            float(name)
        except ValueError:
            self.name = str(name)
        else:
            print("Invalid variable name given, can not be number")
            sys.exit()

    def __str__(self):
        return self.name

    def string(self, type):
        return self.name


class add(parentFunction):
    arglen = None

    def call(self, *args):
        res = 0
        for obj in args[0]:
            res += obj
        return res

    def string(self, *args):
        """
        Slengte sammen en rask stringer for add.
        Den er veldig spesialisert, og vil ikke lett kunne utvides til annet.
        Må bruke litt mer tid på det.
        Er for sulten til å gjøre noe med det akuratt nå :)
        """
        resdic = {"number": 0}
        structure = self.init_structure

        while structure != []:
            obj = structure[0]

            if isinstance(obj, Variable):
                if str(obj) not in resdic:
                    resdic[str(obj)] = 1
                else:
                    resdic[str(obj)] += 1
            elif isinstance(obj, number):
                resdic["number"] += obj

            structure = structure[1:]

        res = ""
        for thing, num in resdic.items():
            if thing == "number" and num != 0:
                res += f"{num} + "
            else:
                res += f"{num}{thing} + "

        return res[:-3]


class sub(parentFunction):
    arglen = 2
    arg_example = "a - b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "sub takes two arguments a,b -> a - b"
        return args[0] - args[1]


class mul(parentFunction):
    arglen = None

    def call(self, *args):
        args = args[0]
        res = 1
        for obj in args:
            res *= obj
        return res


class div(parentFunction):
    arglen = 2
    arg_example = "a / b"

    def call(self, *args):
        args = args[0]
        # assert len(args) == 2, "div takes two arguments a,b -> a/b"
        return args[0] / args[1]


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


class pow(parentFunction):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        return args[0] ** args[1]

    def string(self, string_arg):
        return f"{string_arg[0]}^{string_arg[1]}"


class sqrt(parentFunction):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        return args[0] ** (1 / 2)

    def string(self, string_arg):
        return f"sqrt({string_arg})"


if __name__ == "__main__":
    x = Variable("x")

    k = mul(1, 2, 3, x, x)
    print(pow(-1, 0.2))
