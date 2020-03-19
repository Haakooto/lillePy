from numbers import Number
from bunch import Bunch

# import LillePy as lp


class Variable(str):
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

    def __repr__(self):
        return self.name


class Struct(dict):
    # def __init__(self, *args, **kwargs):
    #     if "weird" in kwargs:
    #         self.weird = True
    #         del kwargs["weird"]
    #     else:
    #         self.weird = False
    #     super().__init__(*args, **kwargs)

    # def exclude_num(self):
    #     tmp = Struct()
    #     for key, val in self.items():
    #         if key != "number":
    #             tmp[key] = val
    #         else:
    #             tmp[key] = 1
    #     return tmp

    def __add__(self, other):
        if isinstance(other, Struct):
            new = Struct({**self, **other})
            for obj, coeff in new.items():
                if obj in self and obj in other:
                    new[obj] = coeff + self[obj]
            return new

        elif "__iter__" not in dir(other):
            if isinstance(other, Number):
                self["number"] += other
            else:
                other = Struct({str(other): 1})
                self += other
            return self
        else:
            print(other, type(other))
            print("something went wrong")
            import sys

            sys.exit()

    def __mul__(self, other):
        if isinstance(other, Struct):
            new = Struct({**self, **other})
            for obj, coeff in new.items():
                if obj in self and obj in other:
                    if obj != "number":
                        new[obj] = coeff + self[obj]
                    else:
                        new[obj] = coeff * self[obj]
            return new
        elif "__iter__" not in dir(other):
            if isinstance(other, Number):
                self["number"] *= other
            else:
                other = Struct({str(obj): 1})
                self *= other
            return self
        else:
            print(other, type(other))
            print("something went wrong")
            import sys

            sys.exit()

    def __pow__(self, other):
        if isinstance(other, Number):
            new = Struct()
            for obj, coeff in self.items():
                new[obj] = coeff * other
            return new
        else:
            print(f"Struct power of type {type(other)} has not yet been implemented!")
            import sys

            sys.exit()

    def __hash__(self):
        return hash(tuple(sorted(self.items())))
