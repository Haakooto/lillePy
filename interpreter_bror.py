import numpy as np


class Interpreter:
    def __init__(self, expr):
        self.expr = expr
        self.make_order0_list()

    def make_order0_list(self):
        self.operator_list = ["+", "-", "*", "/"]
        self.constructor = []
        for symb in self.expr:
            self.constructor.append(symb)

        # print(self.constructor, self.constructor_type)
        self.make_oder1_list()

    def make_oder1_list(self):
        muldiv_list = []
        opr_type_dict = {"+": "add", "-": "sub", "*": "mul", "/": "div", "^": "pow"}

        # this first loop does all the powers

        # this second loop does all the multiplicaiton and division

        dummy = []
        dummy_empty = True
        custom_remove = [False, None]
        prev_opr = None
        for i, obj in enumerate(self.constructor):

            if obj in ["*", "/"]:
                opr = opr_type_dict[obj]

                if dummy_empty:
                    if prev_opr in ["mul", "div"]:
                        dummy = [opr, dummy, self.constructor[i + 1]]
                    else:
                        dummy.append(
                            [opr, self.constructor[i - 1], self.constructor[i + 1]]
                        )
                    dummy_empty = False

                else:
                    if prev_opr in ["mul", "div"]:
                        dummy = [opr, dummy, self.constructor[i + 1]]
                    else:
                        dummy.append(
                            [opr, self.constructor[i - 1], self.constructor[i + 1]]
                        )
                prev_opr = opr

            try:
                if obj in self.operator_list and obj not in ["*", "/"]:
                    prev_opr = None
            except:
                pass
        print(dummy)

        # this third  loop does all addidtion and subtraction
        expr_list = []
        for i, opr in enumerate(self.constructor):
            if expr_list == []:
                expr_empty = True
            # print(opr)
            if opr in ["add", "sub"]:

                if expr_empty:
                    expr_list.append(
                        [opr, self.constructor[i - 1], self.constructor[i + 1]]
                    )
                    expr_list = expr_list[0]
                    expr_empty = False
                else:
                    expr_list = [opr, expr_list, self.constructor[i + 1]]
            else:
                expr_list.append(self.constructor[i])

        print(expr_list)


expression = "1*2+3*4"
test = Interpreter(expression)
