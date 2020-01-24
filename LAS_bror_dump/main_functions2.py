from interpreter_bror import *
if __name__ == '__main__':
    from custom_functions import *
    from numbers import Number
    import sys
import numpy as np

class Variable:
    def __init__(self, name='x'):
        self.name = str(name)
    def __str__(self):
        return self.name
    def __call__(self, *args):
        return args[0]

class parentFunction:
    def __init__(self):
        pass

class add(parentFunction):
    def __init__(self, *args):
        assert len(args) > 1, '"add" takes more than 1 argument!'
        self.arg = list(args)


    def __str__(self):
        print('__str__ called')
        try:
            #this will only succeed if x is undefined
            return str(self.__call__())
        except:
            #this wil call the visible variety of the function
            return_str = 'add('
            for arg in self.arg:
                return_str += str(arg) +','
            return return_str[:-1] + ')'

    def __call__(self, *var):
        print('__call__ called')
        try:
            var = var[0]
        except:
            var = None
        res = 0
        if var is None:
            for arg in self.arg:
                if isinstance(arg, numbers.Number):
                    res += arg
                elif isinstance(arg, parentFunction):
                    res += arg.__call__()
                elif isinstance(arg, Variable):
                    sys.exit(1)
            return res
        else:
            for arg in self.arg:
                if isinstance(var, numbers.Number):
                    res += var
                elif isinstance(var, Variable):
                    res += var
            return res


x = Variable()
opr = add(1,2,add(2,x, 3, 2), add(2,3))

print(opr(1))
