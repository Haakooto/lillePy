import numpy as np
import sys
from numbers import Number

from .Variable import Variable, Struct
from .parents import parentFunction, parentOperator


class add(parentOperator):
    arglen = None

    def call(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            res += obj * coeff

        return res

    def string(self, *args):
        res = ""
        for thing, coeff in self.structure.items():
            if thing == "number" and coeff != 0:
                res += str(coeff)
            if isinstance(thing, Variable):
                if res != "":
                    res += " + "
                if coeff == 1:
                    res += f"{str(thing)}"
                else:
                    res += f"{str(coeff)}{str(thing)}"
            if (isinstance(thing, parentFunction)) or (
                isinstance(thing, parentOperator)
            ):
                if res != "":
                    res += " + "
                if coeff == 1:
                    res += f"{str(thing)}"
                else:
                    res += f"{str(coeff)}{str(thing)}"

        return res


class sub(add):
    arglen = 2
    arg_example = "a - b"

    def __init__(self, *init_structure):
        init = list(init_structure)
        try:
            init[1] = -init[1]
        except:
            print("go die")
        self.init(init)


class mul(parentOperator):
    arglen = None
    null_value = 1

    def call(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            res *= obj ** coeff

        return res

    def string(self, *args):
        res = ""
        for thing, coeff in self.structure.items():
            if thing == "number" and coeff != 0:
                res += str(coeff)
            if isinstance(thing, Variable):
                if res != "":
                    res += "*"

                if coeff == 1:
                    res += f"{str(thing)}"
                else:
                    from .subandsuperscript import superscript

                    res += f"{str(thing)}{superscript(str(coeff))}"
            if (isinstance(thing, parentFunction)) or (
                isinstance(thing, parentOperator)
            ):
                if res != "":
                    res += "*"

                if isinstance(thing, add) and len(thing.structure) > 1:
                    if coeff == 1:
                        res += f"({str(thing)})"
                    else:
                        from .subandsuperscript import superscript

                        res += f"({str(thing)}){superscript(str(coeff))}"
                else:
                    if coeff == 1:
                        res += f"{str(thing)}"
                    else:
                        from .subandsuperscript import superscript

                        res += f"{str(thing)}{superscript(str(coeff))}"

        return res


class div(parentOperator):
    arglen = 2
    arg_example = "a / b"

    def __init__(self, *init_structure):
        init = list(init_structure)


class pow(parentOperator):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        return args[0] ** args[1]

    def string(self, string_arg):
        return f"{string_arg[0]}^{string_arg[1]}"


class sqrt(parentOperator):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        return args[0] ** (1 / 2)

    def string(self, string_arg):
        return f"sqrt({string_arg})"
