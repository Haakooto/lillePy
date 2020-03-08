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

class pow(parentOperator):
    arglen = 2
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