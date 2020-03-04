import numpy as np
import sys
from numbers import Number
from .Variable import Variable, Struct


class parentFunction:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None
    null_value = 0  # default for add

    def __init__(self, *init_structure):
        self.structure = Struct({"number": self.null_value})

        for obj in init_structure:
            if isinstance(obj, Number):
                self.structure["number"] = type(self).call(
                    self, self.structure["number"], obj
                )
            elif obj in self.structure:
                self.structure[obj] += 1
            else:
                self.structure[obj] = 1

        self.call_arg = None
        self.validate_init_structure()

        # # the following is a bugfix that enables layering of anonymous functions
        # for i, obj in enumerate(self.init_structure):
        #     if isinstance(obj, parentFunction):
        #         if (
        #             False
        #             in [isinstance(substruc, number) for substruc in obj.init_structure]
        #         ) is False:
        #             # This is TRUE if theres a function in the init_structure that only has
        #             # numbers in its own init_structure. i.e it's a function with a numeric value
        #             self.init_structure[i] = obj.call(obj.init_structure)

    def __call__(self, **kwargs):
        res = self.null_value

        for thing, coeff in self.structure.items():
            if isinstance(thing, parentFunction):
                # print("parent")
                res = self.call(thing(kwargs), coeff=coeff, res=res)
            elif isinstance(thing, Variable):
                # print("var")
                if Variable in kwargs:
                    res = self.call(kwargs[thing], coeff=coeff, res=res)
                else:
                    """
                    This is for multivariable functions where variables should be set in call
                    f(a=2,r=4, x=np.linspace(0,1,11))
                    Could also be used for implisit variable calling, one or two
                    variable functions where we dont bother typing f(x=1,y=2)

                    For now defaults all variables to value of first val in kwargs
                    """
                    var = list(kwargs.values())[0]
                    res = self.call(var, coeff=coeff, res=res)
            elif thing == "number":
                # print("numnum")
                res = self.call(coeff, res=res)

        return res

    def __str__(self):
        return "YEETING: Youshua-Elizian Extra-Terrestrial Inpastic-Normalized Graphisoding"
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
        print("Get OUT of my HEAD!")
        return None
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
        n = len(self.structure)
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
            False in [isinstance(obj, number) for obj in self.init_structure]
        ) is False
