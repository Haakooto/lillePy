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
        return self.string(None)

    def __repr__(self):
        return self.name


class Struct(dict):
    # def __init__(self, *args, **kwargs):
    # super().__init__(kwargs)
    # self.name = "noname"

    def __add__(self, other):
        if isinstance(other, Struct):
            new = Struct({**self, **other})
            new.name = self.name
            for obj, coeff in new.items():
                if obj in self and obj in other:
                    new[obj] = coeff + self[obj]
            return new
        else:
            print(other, type(other))

    def __mul__(self, other):
        return self + other

    # def __str__(self):
    # return f"{self.name}: {str(dict(self))}"


# x = Variable("x")

# a = Struct()
# a["A"] = 1
# b = Struct()
# b["B"] = 2
# print(a + b)
