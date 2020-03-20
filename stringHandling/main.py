import string as s
import sys
import function as function
from numbers import Number

global local_user_dict
import os


# from ..__init__ import local_user_dict


def listToString(l):
    assert type(l) == list, f"expected type list, got {type(l)}"
    l = removeNestings(l)
    res = ""
    for i in l:
        res += str(i)
    return res


def countNestings(l, count=0):

    for i in l:
        if type(i) == list:

            count = countNestings(i, count + 1)
    return count


def removeNestings(nestedList):
    """ Converts a nested list to a flat list """
    flatList = []
    # Iterate over all the elements in given list
    for elem in nestedList:
        # Check if type of element is list
        if isinstance(elem, list):
            # Extend the flat list by adding contents of this element (list)
            flatList.extend(removeNestings(elem))
        else:
            # Append the elemengt to the list
            flatList.append(elem)

    return flatList


def string_is_number(obj):
    try:
        float(obj)
        return True
    except ValueError:
        return False


class stringHandler:
    """A comprehensive string handler that will convert a string
        from user input to a function of lillepy-type"""

    function_names = dir(function)
    for deletion in [
        # "Bunch",  # Dont think we use this
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
            except IndexError:
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

    def following_segment_is_user_local(self, index, local_user_dict):
        # currently not implemented
        for key in local_user_dict.keys():
            if (key in self.string[index:]) and (key[0] == self.string[index]):
                return True, key
        else:
            return False, None

    def splitted_list(self, local_user_dict):
        if debug:
            print(f"len(string): {len(self.string)}")
        i = 0
        while True:
            # co is short for current object
            if debug:
                print(
                    f"routine string[{i}]={self.string[i]}, splitted_expression = {self.splitted_expression}"
                )
            co = self.string[i]
            if co in ["+", "-", "/", "*", "÷"]:
                self.splitted_expression.append(co)
                i += 1
            elif string_is_number(co):
                # fo is short for following objects
                if debug:
                    print(co, "string_is_number")
                fo = self.number_segment(i)
                self.splitted_expression.append(eval(fo))
                i += len(fo)

            elif self.following_segment_is_user_local(i, local_user_dict)[0]:
                local = self.following_segment_is_user_local[1]
                self.splitted_expression.append(local)
                i += len(local)
            elif self.following_segment_is_function(i):
                if debug:
                    print(self.string[i], "following_segment_is_function")
                fname, fexpr = self.function_segment(i)
                self.splitted_expression.append(fname)
                self.splitted_expression.append(list(fexpr))
                # we now increase the index i by the length of our total function
                a = len(fname)
                b = len(self.string[i + a : self.find_closing_parenthesis(i + a) + 1])
                i += a + b

            elif self.string[i] == "(":
                par0_index = i
                par1_index = self.find_closing_parenthesis(i)
                dummy_instance = stringHandler(self.string[par0_index + 1 : par1_index])
                self.splitted_expression.append(dummy_instance.splitted_list())

                i += len(self.string[par0_index : par1_index + 1])

            else:
                print(f"ERROR string[{i}]={self.string[i]}")
                print(
                    "This message wil only appear if something critical is wrong with the string handling method. Even though the result may sometimes appear correct, this needs to be fixed"
                )
                break
            if i == len(self.string):
                break
        return self.splitted_expression


debug = False
if __name__ == "__main__":
    uin = "23*(5*sin(23))"
    w = stringHandler(uin)
    print(w.splitted_list())

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
