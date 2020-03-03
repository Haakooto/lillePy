import numpy as np
import sys
from numbers import Number as number
from .Variable import Variable


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
