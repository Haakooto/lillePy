import string as s
import sys
import function as function


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


uin = "cos(x)"

for word in dir(function):

    if str(word) in uin:
        index1 = uin.index(word)
        index2 = find_closed_parenthesis(uin, index1 + len(str(word)))
        function_structure = uin[index1 + len(str(word)) + 1 : index2]
        x = function.Variable("x")
        f = eval(f"function.{str(word)}({function_structure})")
        uin = f
        break


print(uin(2))
# from function import *
