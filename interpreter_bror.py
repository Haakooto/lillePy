import numpy as np


class Interpreter:
    def __init__(self, expr):
        self.expr = expr
        self.make_order0_list()

    def make_order0_list(self):
        operator_list = ["+", "-", "*", "/"]
        self.constructor = []
        self.constructor_type = []
        for symb in self.expr:
            if symb in operator_list:
                self.constructor_type.append("operator")
            else:
                try:
                    int(symb)
                    self.constructor_type.append("number")
                except:
                    self.constructor_type.append("variable")
            self.constructor.append(symb)

        print(self.constructor, self.constructor_type)
        self.make_oder1_list()

    def make_oder1_list(self):
        muldiv_list = []
        opr_type_dict = {"+": "add", "-": "sub", "*": "mul", "/": "div"}

        # this firts loop does all the multiplicaiton and division

        dummy = []
        custom_remove = [False, None]
        for i, obj in enumerate(self.constructor):

            if obj in ["*", "/"]:
                dummy.append(
                    [
                        opr_type_dict[obj],
                        self.constructor[i - 1],
                        self.constructor[i + 1],
                    ]
                )
                custom_remove = [True, len(dummy) - 1]
            else:
                try:
                    dummy.append(opr_type_dict[obj])
                except:
                    dummy.append(obj)
                if custom_remove[0]:
                    del dummy[custom_remove[1] - 1]
                    del dummy[custom_remove[1] + 1 - 1]
                    custom_remove = [False, None]
        self.constructor = dummy
        print(self.constructor)

        # this second loop does all addidtion and subtraction
        expr_list = []
        for i, opr in enumerate(self.constructor):
            if expr_list == []:
                expr_empty = True
            print(opr)
            if opr in ["add", "sub"]:

                if expr_empty:
                    expr_list.append(
                        [opr, self.constructor[i - 1], self.constructor[i + 1]]
                    )
                    expr_list = expr_list[0]
                    expr_empty = False
                else:
                    expr_list = [opr, expr_list, self.constructor[i + 1]]

        print(expr_list)

        # print(expr_list)


expression = "1*x-9+x/2+8"
test = Interpreter(expression)
