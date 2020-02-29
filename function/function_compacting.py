from main_functions import *
from Variable import Variable
from parentFunction import parentFunction
from sympy import primefactors


class Compaction:
    # the idea behind the compaction class is that there will be several different types of
    # ways to compact a function. Some may require special attention to the additions,
    # some to the trigonometric, etc. Different types of compactions with different
    # 'settings' will therefore allow for exactly this
    def __init__(self, init_function):
        assert isinstance(
            init_function, parentFunction
        ), f'excpected type "parentFunction", got {type(init_function)}'
        self.init_function = init_function
        self.init_structure = init_function.init_structure

    def join_add_elements(self):
        same_func_dict = {}
        new_init_structure = self.init_structure[:]
        for i, obj1 in enumerate(new_init_structure):
            for obj2 in self.init_structure[i:]:
                if check_if_equal_functions(obj1, obj2):
                    if obj1 not in same_func_dict:
                        same_func_dict[obj1] = 1
                    else:
                        same_func_dict[obj1] += 1

                    del new_init_structure[i]
        for thing, num in same_func_dict.items():
            new_init_structure.append(mul(num, thing))
        self.init_function.init_structure = new_init_structure

    def join_mul_elements(self):
        same_func_dict = {}
        new_init_structure = self.init_structure[:]
        for i, obj1 in enumerate(new_init_structure):
            for obj2 in self.init_structure[i:]:
                if check_if_equal_functions(obj1, obj2):
                    if obj1 not in same_func_dict:
                        same_func_dict[obj1] = 1
                    else:
                        same_func_dict[obj1] += 1

                    del new_init_structure[i]
        for thing, num in same_func_dict.items():
            new_init_structure.append(pow(thing, num))
        self.init_function.init_structure = new_init_structure
        print(new_init_structure, new_init_structure[-1])

    def reorder_div_elements(self):
        new_init_structure = self.init_structure[:]
        obj1, obj2 = tuple(self.init_structure)
        assert (
            self.init_function.__class__ == div
        ), f'expected funciton fype "div", got {self.init_function.__class__}'
        if isinstance(obj1, div):
            new_init_structure[0] = obj1.init_structure[0]
            new_init_structure[1] = mul(obj2, obj1.init_structure[1])
        if isinstance(obj2, div):
            new_init_structure[0] = mul(new_init_structure[0], obj2.init_structure[1])
            new_init_structure[1] = mul(new_init_structure[1], obj2.init_structure[0])

    def factorize_variables_in_divisions(self):
        # this supports multiple variables.
        # This will remove any variables that are in the enumerator and denominator in
        # a division. Recomended ot use after reorder_div_elements()
        assert (
            self.init_function.__class__ == div
        ), f'expected funciton fype "div", got {self.init_function.__class__}'
        # For now this only works with mul() elements in the denominator and enumerator
        for a in self.init_structure:
            print(type(a))
            multiply_numbers_in_mul(a)
        enumerator, denominator = tuple(self.init_structure)[:]

        if (isinstance(enumerator, mul)) and (isinstance(denominator, mul)):
            for i, obj in enumerate(enumerator.init_structure):
                if isinstance(obj, number):
                    enumerator.init_structure[i] = primefactors(obj)
            for i, obj in enumerate(enumerator.init_structure):
                if isinstance(obj, number):
                    enumerator.init_structure[i] = primefactors(obj)

            for i in enumerator.init_structure[:]:
                if i in denominator.init_structure:
                    enumerator.init_structure.remove(i)
                    denominator.init_structure.remove(i)
            multiply_numbers_in_mul(enumerator)
            multiply_numbers_in_mul(denominator)
            self.init_structure = [
                enumerator.init_structure,
                denominator.init_structure,
            ]


def check_if_equal_functions(func1, func2):
    if isinstance(func1, parentFunction) == isinstance(func2, parentFunction) == True:
        # there are several ways to a funct|ion can be equal
        # the first if if they are literally the same instance of a class:
        if func1 == func2:
            return True
        # the second case is if the function is of the same class and has same
        # init_structure(but are different instances)

        if (func1.__class__ == func2.__class__) and (
            func1.init_structure == func2.init_structure
        ):
            return True

    # we need more tests here

    # if all fails, we return a negative
    return False


def multiply_numbers_in_mul(func):
    print(func.__class__, "as")
    assert isinstance(func, mul), "excpected mul"
    res = 1
    for obj in func.init_structure[:]:
        if isinstance(obj, number):

            func.init_structure.remove(obj)
            res *= obj

    func.init_structure.append(res)


if __name__ == "__main__":

    x = Variable("x")
    o = Variable("o")
    j = div(mul(1, 2, 3), mul(2, 3))
    print(j(2))
    c = Compaction(j)
    c.factorize_variables_in_divisions()

    print(j)
