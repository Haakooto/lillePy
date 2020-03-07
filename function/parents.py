import numpy as np
import sys
from numbers import Number as Number

from .Variable import Variable, Struct

# from .parentOperator import parentOperator


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
                    in [isinstance(substruc, Number) for substruc in obj.init_structure]
                ) is False:
                    # This is TRUE if theres a function in the init_structure that only has
                    # numbers in its own init_structure. i.e it's a function with a numeric value
                    self.init_structure[i] = obj.call(obj.init_structure)

    def __call__(self, *args):
        self.call_arg = args[0]

        if isinstance(self.call_arg, Variable):
            return self
        elif isinstance(self.call_arg, Number):
            assert len(args) == 1, "Only takes 1 input"
            self.call_arg = args[0]
            init_structure_variables_replaced = self.replace_variables_with_number(
                self.call_arg
            )
            print(self.init_structure)
            return self.call(init_structure_variables_replaced)

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

    def replace_variables_with_number(self, replacee):
        init_structure_variables_replaced = []

        for obj in self.init_structure:

            if isinstance(obj, parentFunction):
                init_structure_variables_replaced.append(obj.__call__(replacee))
            elif isinstance(obj, parentOperator):
                pass

            elif isinstance(obj, Variable):
                init_structure_variables_replaced.append(replacee)
            elif isinstance(obj, Number):
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
            False in [isinstance(obj, Number) for obj in self.init_structure]
        ) is False


class parentOperator:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None
    null_value = 0  # default for add

    def __init__(self, *init_structure):
        self.init(init_structure)

    def init(self, *init_structure):
        self.original_structure = list(*init_structure)
        self.structure = Struct({"number": self.null_value})

        for obj in self.original_structure:
            self.append_to_structure(obj)

        self = self.validate_init_structure()

    def append_to_structure(self, obj):
        if isinstance(obj, Number):
            self.structure["number"] = type(self).call(
                self, self.structure["number"], obj
            )
        elif obj in self.structure:
            self.structure[obj] += 1
        else:
            self.structure[obj] = 1

    def __call__(self, *args):

        res = self.null_value
        arg = args[0]
        if isinstance(arg, Variable):
            return self
        for thing, coeff in self.structure.items():
            if isinstance(thing, parentOperator):
                res = self.call(thing(arg), coeff=coeff, res=res)
            elif isinstance(thing, parentFunction):
                print(res, "s")
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

    def validate_init_structure(self):
        return True
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
        if self.__class__ == pther.__class__:
            if self.structure == other.structure:
                return True
        return False

    def __hash__(self):
        return 
        # return hash(self.structure)
