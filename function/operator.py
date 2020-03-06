import numpy as np
import sys
from numbers import Number
from .Variable import Variable, Struct


class Operator:
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

class add(Operator):
    arglen = None

    def call(self, *args, **kwargs):
        # print(args, kwargs)
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            # print(res, "before")
            res += obj * coeff
            # print(res, "after")

        return res  # * coeff

    def string(self, *args):
        print("NOPE")
        return "Leslie"
        resdic = {"number": 0}
        structure = self.init_structure

        while structure != []:
            obj = structure[0]

            if isinstance(obj, Variable):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
            elif isinstance(obj, number):
                resdic["number"] += obj
            elif isinstance(obj, Operator):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
                for obj2 in resdic:
                    pass

            structure = structure[1:]
        print(resdic)
        res = ""
        for thing, num in resdic.items():
            if thing == "number" and num != 0:
                res += f"{num} + "
            else:
                if num != 1:
                    res += f"{num}{str(thing)} + "
                else:
                    res += f"{str(thing)}"

        return res[:-3]


class sub(Operator):
    arglen = 2
    arg_example = "a - b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "sub takes two arguments a,b -> a - b"
        return args[0] - args[1]


class mul(Operator):
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

        return res  # ** coeff

    def string(self, *args):
        return "Yop"
        resdic = {"number": 0}
        structure = self.structure

        while structure != []:
            obj = structure[0]

            if isinstance(obj, Variable) or isinstance(obj, Operator):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
            elif isinstance(obj, number):
                resdic["number"] += obj

            structure = structure[1:]

        res = ""
        for thing, num in resdic.items():
            if thing == "number" and num != 1:
                res += f"{num} * "
            else:
                if num != 1:

                    res += f"{str(thing)}^{num} * "
                else:

                    res += f"{str(thing)} * "

        return res[:]


class div(Operator):
    arglen = 2
    arg_example = "a / b"

    def call(self, *args):
        args = args[0]
        # assert len(args) == 2, "div takes two arguments a,b -> a/b"
        return args[0] / args[1]

    def string(self, *args):
        return "TEMPORARY DIV STRING"

class pow(Operator):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        return args[0] ** args[1]

    def string(self, string_arg):
        return f"{string_arg[0]}^{string_arg[1]}"


class sqrt(Operator):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        return args[0] ** (1 / 2)

    def string(self, string_arg):
        return f"sqrt({string_arg})"
