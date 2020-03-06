from .main_functions import *
from .Variable import Variable
from .parentFunction import parentFunction
from sympy import primefactors


def join_add_elements(function):
    assert isinstance(function, add), f"excpected type add got {type(function)}"

    same_func_dict = {}
    new_structure = function.structure[:]
    for i, obj1 in enumerate(new_structure):
        for obj2 in new_structure[i:]:
            if check_if_equal_functions(obj1, obj2):
                if obj1 not in same_func_dict:
                    same_func_dict[obj1] = 1
                else:
                    same_func_dict[obj1] += 1

                del new_structure[i]
    for thing, num in same_func_dict.items():
        new_structure.append(mul(num, thing))

    function.structure = new_structure


def join_mul_elements(function):
    assert isinstance(function, mul), f"excpected type mul got {type(function)}"

    same_func_dict = {}
    new_structure = function.structure[:]
    for i, obj1 in enumerate(new_structure):
        for obj2 in new_structure[i:]:
            if check_if_equal_functions(obj1, obj2):
                if obj1 not in same_func_dict:
                    same_func_dict[obj1] = 1
                else:
                    same_func_dict[obj1] += 1

                del new_structure[i]
    for thing, num in same_func_dict.items():
        new_structure.append(pow(thing, num))

    function.structure = new_structure

    assert isinstance(
        function, parentFunction
    ), f"excpected type parentFunction got {type(function)}"
    same_func_dict = {}
    new_structure = function.structure[:]
    for i, obj1 in enumerate(new_structure):
        for obj2 in function.structure[i:]:
            if check_if_equal_functions(obj1, obj2):
                if obj1 not in same_func_dict:
                    same_func_dict[obj1] = 1
                else:
                    same_func_dict[obj1] += 1

                del new_structure[i]
    for thing, num in same_func_dict.items():
        new_structure.append(pow(thing, num))
    function.structure = new_structure


def reorder_div_elements(function):
    assert isinstance(
        function, parentFunction
    ), f"excpected type parentFunction got {type(function)}"
    new_structure = function.structure[:]
    obj1, obj2 = tuple(function.structure)
    assert (
        self.init_function.__class__ == div
    ), f'expected funciton fype "div", got {function.init_function.__class__}'
    if isinstance(obj1, div):
        new_structure[0] = obj1.structure[0]
        new_structure[1] = mul(obj2, obj1.structure[1])
    if isinstance(obj2, div):
        new_structure[0] = mul(new_structure[0], obj2.structure[1])
        new_structure[1] = mul(new_structure[1], obj2.structure[0])


def defactorize_numbers(function):
    # this will de-factorize the numbers of a function. i.e make
    # 24sin(x) to 2*2*2*3*sin(x).
    assert isinstance(
        function, parentFunction
    ), f"excpected type parentFunction got {type(function)}"


def check_if_equal_functions(func1, func2):
    # this next line checks if the called elements are the same variables
    if (func1 == func2) and isinstance(func1, Variable):
        return True
    if isinstance(func1, parentFunction) == isinstance(func2, parentFunction) == True:

        # there are several ways to a funct|ion can be equal
        # the first if if they are literally the same instance of a class:
        if func1 == func2:
            return True
        # the second case is if the function is of the same class and has same
        # structure(but are different instances)
        # it is allso possible that the init_structure of two functions are the
        # same even though their structure arent (as they may have been heavily modified)
        if (
            (func1.__class__ == func2.__class__)
            and (func1.structure == func2.structure)
        ) or (
            (func1.__class__ == func2.__class__)
            and (func1.init_structure == func2.init_structure)
        ):
            return True

    # we need more tests here

    # if all fails, we return a negative

    return False


def multiply_numbers_in_mul(func):
    print(func.__class__, "as")
    assert isinstance(func, mul), "excpected mul"
    res = 1
    for obj in func.structure[:]:
        if isinstance(obj, number):

            func.structure.remove(obj)
            res *= obj

    func.structure.append(res)


if __name__ == "__main__":

    x = Variable("x")
    a = add(x, x, x, mul(x, x, 2), 1, 2, x, sin(x), 2, sin(x))

    join_add_elements(a)
    print(a.structure)
