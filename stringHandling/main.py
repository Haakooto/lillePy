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


def find_closing_parenthesis(string, index):
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


def number_segment(string, index):
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


def segment_is_function(string, index):
    # currently all functions need to use ().
    try:
        par0_index = string[index:].index("(") + index

        if string[index:par0_index] in function_names:
            return True

    except:
        return False


def function_segment(string, index):
    par0_index = string[index:].index("(") + index

    par1_index = find_closing_parenthesis(string, par0_index)
    print(string[par0_index + 1 : par1_index], "as")
    return (
        f"{string[index:par0_index]}",
        splitter(string[par0_index + 1 : par1_index]),
    )


def segment_is_local(string, index):
    return False


def splitter(string):
    splitted_expression = []
    var = "x"
    i = 0
    while True:
        # co is short for current object
        co = string[i]
        if co in [var, "+", "-", "/", "*", "÷"]:
            splitted_expression.append(co)
            i += 1
        elif string_is_number(co):
            # fo is short for following objects
            fo = number_segment(string, i)
            splitted_expression.append(eval(fo))
            i += len(fo)
            print("hey", string)
        # elif segment_is_local(string, i):
        #    pass
        elif segment_is_function(string, i):
            dummy = function_segment(string, i)
            fname = dummy[0]
            fexpr = dummy[1]  # might be a nested lsit itself
            splitted_expression.append(fname)
            splitted_expression.append(list(fexpr))
            length_of_function = (
                len(fname) + getSizeOfNestedList(fexpr) + 2
            )  # 2 for the ()'s
            i += length_of_function + 1
        # elif co == "(":
        #     print(string, i)
        #     closing_index = find_closing_parenthesis(string, i)
        #     splitted_expression.append(splitter(string[i + 1 : closing_index]))
        #     i += closing_index - i

        else:
            print(co)
            i += 1
        if i == len(string):
            break
    return splitted_expression


"""FOR Å FIKSE DUPLIKERING AV DE SISTE ELEMENTENE, MÅ DU SKRIVE OM DEET OVER TIL
EN KLASSE. DET ER FEIL FORDI ALLE NESTED ELEMENTER ENDRER PÅ SAMME LISTE SOM DERES SUPER"""
uin = "sin(sin(cos(987654321))))"
print(splitter(uin))
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
