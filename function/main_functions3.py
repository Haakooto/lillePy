import numpy as np
import sys
from numbers import Number as number


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
    def __init__(self, *init_structure):
        self.init_structure = list(init_structure)

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

    def __str__(self):
        if "string" in dir(self):
            return self.string()
        else:
            print(f"Printing has not yet been implemented here")


class add(parentFunction):
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
    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "sub takes two arguments a,b -> a - b"
        return args[0] - args[1]


class mul(parentFunction):
    def call(self, *args):
        args = args[0]
        res = 1
        for obj in args:
            res *= obj
        return res


class div(parentFunction):
    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "div takes two arguments a,b -> a/b"
        return args[0] / args[1]


class cos(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "cos takes 1 argument a -> cos(a)"
        return np.cos(arg[0])


class sin(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "sin takes 1 argument a -> sin(a)"
        return np.sin(arg[0])


class ln(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "ln takes 1 argument a -> ln(a)"
        return np.log(arg[0])


class log(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "log takes 1 argument a -> log(a)"
        return np.log10(arg[0])


class pow(parentFunction):
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
    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        try:
            return args[0] ** (1 / 2)
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)


if __name__ == "__main__":
    x = Variable("x")
    f = add(x, x, x, 2, 4, mul(x, x))
    print(f)
    # a = cos(x)
    # b = sin(x)
    # s = sin(x)
    # c = cos(x)
    # tan = div(sin(x), cos(x))
    # t = sqrt(add(1, mul(-1, tan(x))))
    # print(t(2))
