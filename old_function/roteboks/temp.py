import numpy as np


class Interpreter:
    def __init__(self, expr):
        self.expr = expr
        self.make_order0_list()

        self.symb_type = {"number": 1, "variable": 2, "operator": 3}
        self.check_validity_of_expression()

        # self.remove_times_one()

    def make_order0_list(self):
        operator_list = ["+", "-", "*", "/"]
        constructor = []
        constructor_type = []
        for symb in self.expr:

            if symb in operator_list:
                constructor_type.append("operator")
            else:
                try:
                    float(symb)
                    constructor_type.append("number")
                except:
                    constructor_type.append("variable")
            constructor.append(symb)

        self.constructor = constructor
        self.constructor_type = constructor_type

    def check_validity_of_expression(self):
        i = 0
        while i < len(self.constructor):
            i += 1
            print(i, self.constructor[i])
            this_type = self.symb_type[self.constructor_type[i]]
            that_type = self.symb_type[self.constructor_type[i - 1]]

            value = this_type * that_type

            if value == 1:
                del self.constructor_type[i + 1]
                self.constructor[i] = self.constructor[i] + self.constructor[i + 1]
                del self.constructor[i + 1]
                print(self.constructor, self.constructor_type)

            elif value == 2:
                self.constructor_type.insert(i + 1, "operator")
                self.constructor.insert(i + 1, "*")

            elif value == 9:
                this_symb = self.constructor[i]
                that_symb = self.constructor[i + 1]
                self.check_valid_double_operator(this_symb, that_symb)

    def check_valid_double_operator(self, this, that):
        pass

    def remove_times_one(self):
        expr_arr = np.asarray(self.constructor)
        ones = np.where(expr_arr == "1")[0]
        times = np.where(expr_arr == "*")[0]

        times_one = False
        for idx in ones:
            if np.any(abs(times - idx) == 1):
                del self.constructor[idx]
                if self.constructor[idx : idx + 1] == ["1", "*"]:
                    del self.constructor[idx + 1]
                elif self.constructor[idx : idx + 1] == ["*", "1"]:
                    del self.constructor[idx - 1]

                times_one = [s for s in self.constructor]
                print(times_one)
                self = Interpreter(times_one)


expression = "21xy+x*1*3"
expression = "2x+3"
test = Interpreter(expression)
print(test.constructor)
print(test.constructor_type)
