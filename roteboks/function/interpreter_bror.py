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
        self.opr_type_dict = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div",
            "^": "pow",
        }

        # this will allow for parenthesis
        constructor = self.constructor[:]
        if "(" in constructor:
            parnt_constructor = []
            for i, obj in enumerate(constructor):

                if obj == "(":
                    par_1 = i
                    j = 1
                    while obj != ")":
                        obj = constructor[i + j]
                        parnt_constructor.append(obj)
                        j += 1
                    par_2 = i + j
                    del parnt_constructor[-1]
                    new = Interpreter(parnt_constructor)

                    constructor[par_1] = new
                    del constructor[par_1:par_2]

        muldiv_construction = self.order1_constructor_builder(
            self.constructor, ["*", "/"]
        )

        # print(muldiv_construction)
        # the following prepares the list for add/sub construction
        constructor_copy = self.constructor[:]
        # print(muldiv_construction)
        """
        for i, obj in enumerate(constructor_copy):
            if obj in ["*", "/"]:
                constructor_copy[i] = muldiv_construction[0]
                print(muldiv_construction, "a")
                del muldiv_construction[0]
                del constructor_copy[i - 1]
                del constructor_copy[i + 1 - 1]
                print(constructor_copy)
        """
        # finally, addsub constrction
        # print(constructor_copy)
        # addsub_construction = self.order1_constructor_builder(
        #    constructor_copy, ["+", "-"]
        # )

        # print(addsub_construction)

    def order1_constructor_builder(self, constructor, operations_symb):
        """
        This general function will construct a list for the given operations
        """
        # IKKE GIT COMMIT! SAMMENLIGN MED DE TO INDIVIDUELLE OPS
        operations = [self.opr_type_dict[i] for i in operations_symb]
        builder = []
        prev_opr = None
        dummy = []
        # for i, obj in enumerate(constructor):

        opr_list = [
            i if x in operations_symb else None for i, x in enumerate(constructor)
        ]
        for i, a in enumerate(opr_list):
            if a is None:
                del opr_list[i]
        print(opr_list)

        for i, a in enumerate(opr_list):
            if a is not None:
                dummy.append(constructor[a - 1])

            else:
                if opr_list[i - 1] is not None:
                    dummy.append(constructor[opr_list[i - 1] + 1])

                if dummy != []:
                    builder.append(dummy)
                dummy = []
        print(builder)
        # print(builder, "a")
        """
                if dummy_empty:
                    if prev_opr in operations:
                        dummy = [opr, dummy, constructor[i + 1]]
                    else:
                        dummy.append([opr, constructor[i - 1], constructor[i + 1]])
                    dummy_empty = False
                else:
                    if prev_opr in operations:
                        dummy = [opr, dummy, constructor[i + 1]]
                    else:
                        dummy.append([opr, constructor[i - 1], constructor[i + 1]])
                prev_opr = opr

            try:
                if obj in self.operator_list and obj not in operations_symb:
                    prev_opr = None
            except:
                pass
        """
        return builder


def listed_nest_remover(l):
    nested_list_dummy = []

    def list_nested_remover_2(l):
        for i in l:
            if isinstance(i, list):
                list_nested_remover_2(i)
            else:
                nested_list_dummy.append(i)

    list_nested_remover_2(l)
    return nested_list_dummy


def index_symbols(string, *symbol):
    symbls = []
    # first find possible symbol to the left:
    lsymb = None
    for i, symb in enumerate(string):
        if symb in list(symbol):
            symbls.append(i)
    return symbls


class Functions:
    def __str__(self):
        passable_string = "("
        for i in self.passed:
            passable_string += str(i) + ","

        passable_string = passable_string[:-1] + ")"

        return self.function_name + passable_string


class add(Functions):
    def __init__(self, *passed):

        self.function_name = "add"
        self.passed = listed_nest_remover(list(passed))
        for i, obj in enumerate(passed):
            if obj == 0:
                del self.passed[i]
                break
        for i, obj in enumerate(passed):
            if isinstance(obj, add):
                if len(self.passed) > 1:
                    del self.passed[-1]
                self.passed = add(self.passed + obj.passed).passed[0]


class mul(Functions):
    def __init__(self, *passed):
        self.function_name = "mul"
        self.passed = list(passed)
        for i, obj in enumerate(passed):
            if isinstance(obj, mul):
                del self.passed[-1]
                self.passed = mul(self.passed + obj.passed).passed[0]


class Interpreter2:
    def __init__(self, base_expr):
        self.base_expr = base_expr
        self.addsub()

    def addsub(self):

        index_operations = index_symbols(self.base_expr, "+", "-")
        print(index_operations)
        for j, index in enumerate(index_operations):

            if j == len(index_operations) - 1:
                addsub_result = add(addsub_result.passed, self.base_expr[index + 1 :])

            elif j == 0:
                addsub_result = add(
                    self.base_expr[0:index],
                    self.base_expr[index + 1 : index_operations[j + 1]],
                )

            else:
                addsub_result = add(
                    addsub_result.passed,
                    self.base_expr[index + 1 : index_operations[j + 1]],
                )

        self.addsub_result = addsub_result

    def __str__(self):
        return str(self.addsub_result)


expression = "A+B+C+cos(x)"
a = add(1, 2, add(3, 2, 5))
print(a)
# test = Interpreter2(expression)
# a = add(1, 2, add(3, 4, add(5, 6)))
# b = mul(a, 7, 8, add("A", "B", mul("C", "D")))

B = Interpreter2(expression)
print(B)
# print(add(add("A"), add("B")))
# print(closest_symbols(expression, 3))
# todo for haakon
# fjerne reduntant parantes
