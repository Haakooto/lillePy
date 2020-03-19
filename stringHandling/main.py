import string as s
import sys
import function as function
from numbers import Number


def getSizeOfNestedList(listOfElem):
    """ Get number of elements in a nested list"""
    count = 0
    # Iterate over the list
    for elem in listOfElem:
        # Check if type of element is list
        if type(elem) == list:
            # Again call this function to get the size of this element
            count += getSizeOfNestedList(elem)
        else:
            count += 1
    return count


def countNestings(l, n=0):
    print(n, l)
    for i in l:
        if type(i) == list:
            return countNestings(i, n=n + 1)

    return n


def string_is_number(obj):
    try:
        float(obj)
        return True
    except:
        return False


class stringHandler:
    """A comprehensive string handler that will convert a string
        from user input to a function of lillepy-type"""

    function_names = dir(function)
    for deletion in [
        "Bunch",
        "Number",
        "Struct",
        "Variable",
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__path__",
        "__spec__",
        "add",
        "basicFunctions",
        "np",
        "operatorFunctions",
        "parentFunction",
        "parentOperator",
        "parents",
        "sys"
        # This list needs to be expanded as new structures are added
    ]:
        function_names.remove(deletion)

    def __init__(self, string):
        self.splitted_expression = []
        self.string = string

        if debug:
            print(self.string, "init string print")

    def find_closing_parenthesis(self, index):
        # this function finds the index of the closing parenthesis in a string
        # index is the index of the parenthesis we wish to find
        # its closed counterpart to
        assert (
            self.string[index] == "("
        ), f'expected symbol "(", got {self.string[index]}'

        # this is how many '(' are between the current parenthesis and the fisr cllsing parenthesis
        start_par_amount = self.string[
            index + 1 : index + self.string[index:].index(")")
        ].count("(")
        j = start_par_amount
        i = 0
        while j >= 0:
            if self.string[index + 1 + i] == ")":
                j -= 1
            i += 1
        return index + i

    def number_segment(self, index):
        res = self.string[index]
        obj = res
        i = 1
        while True:
            try:
                obj = self.string[index + i]
            except:
                break
            if (not string_is_number(obj)) and (obj != "."):
                break
            res += obj
            i += 1
        if res.count(".") > 1:
            print(f"Error, check decimal points in {self.string} around index {i}")
            sys.exit(1)
        return res

    def function_segment(self, index):
        par0_index = self.string[index:].index("(") + index

        par1_index = self.find_closing_parenthesis(par0_index)

        if debug:
            print(self.string[par0_index + 1 : par1_index], "part sent into handler")

        dummy_instance = stringHandler(f"{self.string[par0_index + 1 : par1_index]}")

        dummy_instance.splitted_list()
        if debug:
            print(
                dummy_instance.splitted_expression,
                "splitted expression returned from splitting",
            )
        return (
            f"{self.string[index:par0_index]}",
            dummy_instance.splitted_expression,
        )

    def following_segment_is_function(self, index):
        # currently all functions need to use ().
        try:
            par0_index = self.string[index:].index("(") + index

            if self.string[index:par0_index] in self.function_names:
                return True
        except:
            return False

    def following_segment_is_local(self, index):
        # currently not implemented
        return False

    def splitted_list(self):
        var = "x"
        i = 0
        while True:
            # print(self.string, "routine, string print")
            # co is short for current object
            if debug:

                print(
                    f"routine string[{i}]={self.string[i]}, splitted_expression = {self.splitted_expression}"
                )
            co = self.string[i]
            if co in [var, "+", "-", "/", "*", "÷"]:
                self.splitted_expression.append(co)
                i += 1
            elif string_is_number(co):
                # fo is short for following objects
                if debug:
                    print(co, "string_is_number")
                fo = self.number_segment(i)
                self.splitted_expression.append(eval(fo))
                i += len(fo)

            # elif segment_is_local(string, i):
            #    pass
            elif self.following_segment_is_function(i):
                if debug:
                    print(self.string[i], "following_segment_is_function")
                dummy = self.function_segment(i)
                fname = dummy[0]
                fexpr = dummy[1]  # might be a nested lsit itself
                self.splitted_expression.append(fname)
                self.splitted_expression.append(list(fexpr))
                # print(fexpr)

                length_of_function = (
                    len(fname) + getSizeOfNestedList(fexpr) + 2 * (countNestings(fexpr))
                )
                if debug:
                    print(f"length of {fname}({fexpr}): {length_of_function}")
                i += length_of_function
            # elif co == "(":
            #     print(string, i)
            #     closing_index = find_closing_parenthesis(string, i)
            #     splitted_expression.append(splitter(string[i + 1 : closing_index]))
            #     i += closing_index - i

            else:
                break
            if i == len(self.string):
                break
        return self.splitted_expression


print(countNestings([123, [34, 4, [4]]], 0))
debug = True
uin = "12+sin(34*cos(56-ln(78)))"
w = stringHandler(uin)
print(w.splitted_list())
# print(splitter(uin))
# for word in dir(function):
#
#     if str(word) in uin:
#         index1 = uin.index(word)
#         index2 = find_closed_parenthesis(uin, index1 + len(str(word)))
#         function_structure = uin[index1 + len(str(word)) + 1 : index2]
#         x = function.Variable("x")
#         f = eval(f"function.{str(word)}({function_structure})")
#         uin = f
#         break
#
#
# print(uin(2))
# from function import *
