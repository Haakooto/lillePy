import numpy as np
import sys
from numbers import Number as Number

from .Variable import Variable, Struct


class parentFunction:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None

    def __init__(self, *init_structure):
        self.init_structure = list(init_structure)[:]
        self.validate_init_structure()
        self.structure = list(init_structure)[:]
        self.call_arg = None

        # the following is a bugfix that enables layering of anonymous functions
        for i, obj in enumerate(self.structure):
            if isinstance(obj, parentFunction):
                if (
                    False
                    in [isinstance(substruc, Number) for substruc in obj.structure]
                ) is False:
                    # This is TRUE if theres a function in the init_structure that only has
                    # numbers in its own structure. i.e it's a function with a numeric value
                    self.structure[i] = obj.call(obj.structure)

    def __call__(self, *args):
        self.call_arg = args[0]

        if isinstance(self.call_arg, Variable):
            return self
        elif isinstance(self.call_arg, Number):
            structure_variables_replaced = self.replace_variables_with_number(
                self.call_arg
            )

            return self.call(structure_variables_replaced)

    def __str__(self):
        return self.string()
        if "string" in dir(self):
            if self.structure_is_numbers():
                return f"{self.call(self.structure)}"
            else:
                if len(self.structure) == 1:
                    return self.string(str(self.structure[0]))
                else:
                    return self.string([str(obj) for obj in self.structure])

        else:
            return f"this function does not have string support yet"

    def replace_variables_with_number(self, replacee):
        structure_variables_replaced = []

        for obj in self.structure:

            if isinstance(obj, parentFunction) or isinstance(obj, parentOperator):
                structure_variables_replaced.append(obj.__call__(replacee))

            elif isinstance(obj, Variable):
                structure_variables_replaced.append(replacee)
            elif isinstance(obj, Number):
                structure_variables_replaced.append(obj)

        return structure_variables_replaced

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

    def structure_is_numbers(self):
        # returns True if all the values in istructure are numbers
        return (False in [isinstance(obj, Number) for obj in self.structure]) is False


class parentOperator:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None
    null_value = 0  # default for add

    def __init__(self, *init_structure):
        self.original_structure = list(init_structure)
        self.structure = Struct({"number": self.null_value})

        self.init()
        self = self.validate_init_structure()

    def init(self):
        for obj in self.original_structure:
            self.append_to_structure(obj)

    def append_to_structure(self, obj, am_sd="am"):
        assert am_sd in ("am", "sd")

        if isinstance(obj, Number):
            self.structure["number"] = type(self).call(
                self, self.structure["number"], obj
            )

        elif isinstance(obj, parentOperator):
            if (
                self.null_value == obj.null_value
            ):  # check if same operator type (add and add, or mul and mul)
                self.structure = type(self).call(
                    self, obj.structure, res=self.structure
                )
            elif self.null_value == 0 and obj.null_value == 1:
                # add and mul
                new = obj.copy()
                coeff = new.structure["number"]
                new.structure["number"] = new.null_value
                if new in self.structure:
                    self.structure[new] += coeff
                else:
                    self.structure[new] = coeff

            elif self.null_value == 1 and obj.null_value == 0:
                # mul and add
                new = obj.copy()
                if new in self.structure:
                    self.structure += 1
                else:
                    self.structure[new] = 1

        elif obj in self.structure:
            if am_sd == "am":
                self.structure[obj] += 1
            else:
                self.structure[obj] -= 1
        else:
            if am_sd == "am":
                self.structure[obj] = 1
            else:
                self.structure[obj] = -1

    def __getitem__(self, num):
        return self.structure

    def res_coeff(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        return res, coeff

    def __call__(self, *args):

        res = self.null_value
        arg = args[0]
        if isinstance(arg, Variable):
            return self
        for thing, coeff in self.structure.items():
            # print(thing, coeff)
            if isinstance(thing, parentOperator):
                res = self.call(thing(arg), coeff=coeff, res=res)
            elif isinstance(thing, parentFunction):
                res = type(self)(thing(arg), res).structure["number"]

            elif isinstance(thing, Variable):
                if isinstance(arg, Variable):
                    res = self.call(arg(thing), coeff=coeff, res=res)
                else:
                    """
                    This is for multivariable functions where variables should be set in call
                    f(a=2,r=4, x=np.linspace(0,1,11))
                    Could also be used for implisit variable calling, one or two
                    variable functions where we dont bother typing f(x=1,y=2)

                    For now defaults all variables to value of first val in kwargs
                    """
                    var = arg
                    res = self.call(var, coeff=coeff, res=res)
            elif thing == "number":
                res = self.call(coeff, res=res)
        return res

    def __str__(self):
        return self.string()

    def repr(self):
        clas = str(self.__class__)[:-2]
        clas = clas[clas.rfind(".") + 1 :]
        return f"({clas}, {self.structure})"

    def __repr__(self):
        return self.repr()

    def copy(self):
        new = type(self)(1, 1)
        new.structure = self.structure.copy()
        return new

    def validate_init_structure(self):

        n = len(self.original_structure)
        if self.arglen is not None:

            msg = (
                f"{self.__class__} takes {self.arglen} arguments, but {n} were given. "
            )
            for l in range(
                97, 97 + self.arglen
            ):  # add n letter from a to msg: a,b,c,...
                msg += f"{chr(l)},"
            msg = msg[:-1] + " -> " + self.arg_example
            assert n == self.arglen, msg
        else:

            assert n > 1, f"{self.__class__} takes at least two arguments"

    def init_structure_are_numbers(self):
        # returns True if all the values in init_structure are numbers
        return (
            False in [isinstance(obj, Number) for obj in self.original_structure]
        ) is False

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.structure == other.structure:
                return True
        return False

    def __hash__(self):
        return hash(self.structure)

    def __add__(self, other):
        import lillePy as lp

        return lp(f"{self} + {other}")

    def __mul__(self, other):
        import lillePy as lp

        return lp(f"({self}) * {other}")

    def __sub__(self, other):
        import lillePy as lp

        return lp(f"{self} - {other}")

    def __div__(self, other):
        import lillePy as lp

        return lp(f"({self}) / {other}")
