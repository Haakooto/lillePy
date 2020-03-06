import numpy as np


class Interpreter:
    symb_type = {"number": 1, "variable": 2, "operator": 3}
    operator_list = ["+", "-", "*", "/"]

    def __init__(self, expr):
        self.original = expr
        self.expr = expr.replace(" ", "")

        self.make_order0_list()
        self.make_oder1_list()

    def make_order0_list(self):
        constructor = []
        constructor_type = []

        # Classify each symbol in expr as number, operator or letter
        for symb in self.expr:
            if symb in self.operator_list:
                constructor_type.append(self.symb_type["operator"])
            else:
                try:
                    float(symb)
                    constructor_type.append(self.symb_type["number"])
                except:
                    constructor_type.append(self.symb_type["variable"])
            constructor.append(symb)

        self.constructor = constructor
        self.constructor_type = constructor_type

        self.reformat_expression()

    def reformat_expression(self):
        def merge_and_del(here):
            self.constructor[here] += self.constructor[here + 1]
            del self.constructor[here + 1]
            del self.constructor_type[here + 1]

        here = 0
        typ = lambda idx: self.constructor_type[here + idx]
        while True:
            try:
                value = typ(0) * typ(1)
            except IndexError:
                break
            else:
                if value == 1:
                    merge_and_del(here)
                elif value == 2:
                    here += 1
                    self.constructor.insert(here, "*")
                    self.constructor_type.insert(here, self.symb_type["operator"])
                elif value == 3:
                    here += 1
                elif value == 4:
                    merge_and_del(here)
                elif value == 6:
                    here += 1
                elif value == 9:
                    self.check_valid_double_operator()

    def check_valid_double_operator(self):
        """For symbols like **, ==, !="""
        pass

    def add_variables(self):
        vars = np.asarray(self.constructor)[
            np.where(np.asarray(self.constructor_type) == 2)
        ]
        self.base._add_variables(vars)

    def make_oder1_list(self):
        # muldiv_list = []
        opr_type_dict = {"+": "add", "-": "sub", "*": "mul", "/": "div", "^": "pow"}

        # this first loop does all the powers

        # this second loop does all the multiplicaiton and division

        dummy = []
        dummy_empty = True
        # custom_remove = [False, None]
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
        self.list = dummy
        # print(dummy)

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

        # print(expr_list)
        self.expr_list = expr_list


expression = "1*2+3*4"
expression = "211vs*3+53*lpets*ts+1"
I = Interpreter(expression)
print(I.expr_list)
# test = Interpreter(expression)


"""
ser ut som det er noe gale med make_order1:
['mul', ['mul', [['mul', '211', 'vs']], '3', ['mul', '53', 'lpets']], 'ts']
['211', '*', 'vs', '*', '3', '+', '53', '*', 'lpets', '*', 'ts', '+', '1']

make_order0 fjerner ikke *1 og +0. Tror det kan være lurt å "evaluere"
hver miniliste fra make_order1; [mul, ["mul", "211", "3"], f] umiddelbart erstattes av [mul, 633, f]
Dette fjerner *1 og +0.
Må bruke Variables-klasse fra LAS for å kunne evaluere variabler med None som verdi
vet ikke hvordan vi gjør med ting som 3*f*2, ettersom den blir [mul, [mul, 3, f], 2]

"""
