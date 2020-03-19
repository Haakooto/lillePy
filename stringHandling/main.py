import string as s
import sys
import function as function
from numbers import Number


function_names = dir(function)
for del_obj in [
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
    function_names.remove(del_obj)


def find_closed_parenthesis(string, index):
    # this function finds the index of the closing parenthesis in a string
    # index is the index of the parenthesis we wish to find
    # its closed counterpart to
    assert string[index] == "(", f'expected symbol "(", got {string[index]}'

    # this is how many '(' are between the current parenthesis and the fisr cllsing parenthesis
    start_par_amount = string[index + 1 : index + string[index:].index(")")].count("(")
    j = start_par_amount
    i = 0
    while j >= 0:
        if string[index + 1 + i] == ")":
            j -= 1
        i += 1
    return index + i


def string_is_number(obj):
    try:
        float(obj)
        return True
    except:
        return False


def segment_is_number(string, index):
    res = string[index]
    obj = res
    i = 1
    while True:
        try:
            obj = string[index + i]
        except:
            break
        if (not string_is_number(obj)) and (obj != "."):
            break
        res += obj
        i += 1
    if res.count(".") > 1:
        print(f"Error, check deciaml points in {string}")
        sys.exit(1)
    return res


def splitter(string):
    splitted_expression = []
    i = 0
    while True:
        # co is short for current object
        co = string[i]
        if string_is_number(co):
            # fo is short for following objects
            fo = segment_is_number(string, i)
            i += len(fo)
            splitted_expression.append(eval(fo))
        elif co in ["+", "-", "/", "*", "÷"]:
            splitted_expression.append(co)
            i += 1
        else:
            i += 1
        if i == len(string):
            break
    return splitted_expression


uin = "234+34556+3.2"
print(splitter(uin))
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
