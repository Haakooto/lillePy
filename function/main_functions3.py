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

    def string(self, type):
        return self.name


class parentFunction:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None

    def __init__(self, *init_structure):
        self.init_structure = list(init_structure)
        self.call_arg = None
        self.validate_init_structure()

        # the following is a bugfix that enables layering of anonymous functions
        for i, obj in enumerate(self.init_structure):
            if isinstance(obj, parentFunction):
                if (
                    False
                    in [isinstance(substruc, number) for substruc in obj.init_structure]
                ) is False:
                    # This is TRUE if theres a function in the init_structure that only has
                    # numbers in its own init_structure. i.e it's a function with a numeric value
                    self.init_structure[i] = obj.call(obj.init_structure)

    def __call__(self, *args):
        self.call_arg = args[0]

        if isinstance(self.call_arg, Variable):
            return self
        elif isinstance(self.call_arg, number):
            assert len(args) == 1, "Only takes 1 input"
            self.call_arg = args[0]
            init_structure_variables_replaced = self.replace_variables_with_number(
                self.call_arg
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

    def init_structure_are_numbers(self):
        # returns True if all the values in init_structure are numbers
        return (
            False in [isinstance(obj, number) for obj in self.init_structure]
        ) is False

    def __str__(self):

        if "string" in dir(self):
            if self.init_structure_are_numbers():
                return f"{self.call(self.init_structure)}"
            else:
                if len(self.init_structure) == 1:
                    return self.string(str(self.init_structure[0]))
                else:
                    return self.string([str(obj) for obj in self.init_structure])

        else:
            return f"this function does not have string support yet"


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
        try:
            return args[0] ** args[1]
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)

    def string(self, string_arg):

        return f"{string_arg[0]}^{string_arg[1]}"


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

    def string(self, string_arg):
        return f"sqrt({string_arg})"


if __name__ == "__main__":
    x = Variable("x")

    k = mul(1, 2, 3, x, x)
    print(k(2))
