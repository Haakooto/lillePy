#import numpy as np
import numbers



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

class Variable:
    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return str(self.var_name)

    def __call__(self, *args):
        print('__call__ in variable')
        assert len(args) == 1
        arg = args[0]
        print(arg)
        return self


class parentFunctions:
    def __init__(self):
        self.x = Variable('x')


    def __str__(self):
        from custom_functions import customFunction, Variable
        print('__str__ called')
        if isinstance(self.passed, numbers.Number):
            print('numbers called')
            return str(self(self.passed))#self.function_name + '(' + str(self.passed) + ')'
        elif isinstance(self.passed, Variable):
            print('variable called')
            return self.function_name + '(' + self.variable.var_name + ')'
        elif isinstance(self.passed, parentFunctions):
            print('parentFunctions called')
            if self.call_exact:
                print('call_exact called')
                if isinstance(self.passed.passed, Variable):
                    print('Variable called')
                    return self.function_name + '(' + self.variable.var_name + ')'
                elif isinstance(self.passed.passed, numbers.Number):
                    print('numbers called')
                    return self.function_name + '(' + str(self.passed.passed) + ')'
                elif isinstance(self.passed.passed, parentFunctions):
                    print('parentFunctions called')
                    return str(self.passed.passed(self.passed.passed.passed))
                else:
                    print('Error')
                    return None

            elif not self.call_exact:
                print('not call_exact called')
            #return self.function_name + '(' + str(self.passed(self.passed.passed)) + ')'

        if isinstance(self.passed, list):
            main_str = self.function_name + '('
            for passed in self.passed:
                main_str += str(passed) + ','
            return main_str[:-1] + ')'



        '''
        print('__str__ called')


        if isinstance(self.variable, Variable):
            print('ho')
            #this will print if the funciton depends on a variable
        def call_once():
            if self.passed == self.variable:
                # if func(x) is called
                return self.function_name + '(' + self.variable.var_name + ')'
            else:
                #if func(2) is called (2 can be any number)
                return self(self.passed)

        try:
            if len(self.passed) > 1:
                for passed in self.passed:
                    if passed == self.variable:
                        return call_once()
                    elif isinstance(passed, parentFunctions):
                        print(passed)
                        return passed(passed.passed)
        except AttributeError:
            if isinstance(self.passed, Variable):
                print(self.passed)
                return self.passed(self.passed.passed)
            else:
                print(self.passed, 'ashuduishrit')
                return self.passed
        return 'FAILURE 2'



        try:
            return self.function_name_super + '(x)'
            #print(self.function_name_super)
        except:
            pass
        passable_string = "("
        try:
            for obj in self.passed:

                if isinstance(obj, customFunction):
                    #passable_string += obj.custom_function_name
                    #print('hey')
                    break
                else:
                    passable_string += str(obj) + ","

            passable_string = passable_string[:-1] + ")"

            return self.function_name + passable_string
        except TypeError:
            print('ha')
            if isinstance(self.passed, Variable):
                return self.function_name + '(' + str(self.passed) + ')'
            elif isinstance(self.passed, numbers.Number):
                return str(self(self.passed))
            elif isinstance(self.passed, parentFunctions):
                return str(self(self.passed(self.passed.passed)))
        '''




if __name__ == '__main__':
    x = Variable('x')
    a = sub(1,1)
    print(a(2))
