import numpy as np
import sys
from numbers import Number as number


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


class parentFunction:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None

    def __init__(self, *init_structure):
        self.init_structure = list(init_structure)
        self.validate_init_structure()

    def __call__(self, *args):
        call_arg = args[0]

        if isinstance(call_arg, Variable):
            return self
        elif isinstance(call_arg, number):
            assert len(args) == 1, "Only takes 1 input"
            call_arg = args[0]
            init_structure_variables_replaced = self.replace_variables_with_number(
                call_arg
            )

            return self.call(init_structure_variables_replaced)

    def replace_variables_with_number(self, replacee):
        init_structure_variables_replaced = []
        for obj in self.init_structure:

            if isinstance(obj, parentFunction):
                init_structure_variables_replaced.append(obj.__call__(replacee))
            elif isinstance(obj, Variable):
                init_structure_variables_replaced.append(replacee)
            elif isinstance(obj, number):
                init_structure_variables_replaced.append(obj)

        return init_structure_variables_replaced

    def validate_init_structure(self):
        n = len(self.init_structure)
        if self.arglen is not None:
            msg = (
                f"{self.__class__} takes {self.arglen} arguments, but {n} were given. "
            )
            for l in range(97, 97 + self.arglen):
                msg += f"{chr(l)},"
            msg = msg[:-1] + " -> " + self.arg_example
            assert n == self.arglen, msg
        else:
            assert n > 1, f"{self.__class__} takes at least two arguments"

    def __str__(self):
        if "string" in dir(self):
            return self.string()
        else:
            print(f"Printing has not yet been implemented here")


class add(parentFunction):
    arglen = None

    def call(self, *args):
        res = 0
        for obj in args[0]:
            res += obj
        return res

    def string(self):
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


class sin(parentFunction):
    arglen = 1
    arg_example = "sin(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "sin takes 1 argument a -> sin(a)"
        return np.sin(arg[0])


class ln(parentFunction):
    arglen = 1
    arg_example = "ln(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "ln takes 1 argument a -> ln(a)"
        return np.log(arg[0])


class log(parentFunction):
    arglen = 1
    arg_example = "log(a)"

    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "log takes 1 argument a -> log(a)"
        return np.log10(arg[0])


class pow(parentFunction):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        try:
            return args[0] ** args[1]
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)


class sqrt(parentFunction):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        try:
            return args[0] ** (1 / 2)
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)


class summation(parentFunction):
    arglen = None

    def call(self, *args):
        print("df")
        # the calling of sum is as follows:
        # sum(sum_var, bottom_val, top_val, sum_func)
        args = args[0]
        assert (
            len(args) == 4
        ), "the calling of sum is as follows: sum(sum_var, bottom_val, top_val, sum_func)"
        sum_var, bottom_val, top_val, sum_func = args
        assert isinstance(sum_var, Variable), 'sum_var is not of instance "Variable"'
        assert isinstance(bottom_val, int), "bottom_val is not an integer"
        assert isinstance(top_val, int), "top_val is not an integer"
        assert isinstance(sum_func, parentFunction), "sum_func is not a function"
        res = 0
        for i in range(bottom_val, top_val + 1):
            res += sum_func(i)
        return res


if __name__ == "__main__":
    x = Variable("x")
    f = add(x, x, x, 2, 4)
    g = div(1, 2)

    # a = cos(x)
    # b = sin(x)
    # s = sin(x)
    # c = cos(x)
    # tan = div(sin(x), cos(x))
    # t = sqrt(add(1, mul(-1, tan(x))))
    # print(t(2))
    # x = Variable
    # n = Variable

    # k = summation()
    # print(k(n, 1, 100, add(1, n)))
