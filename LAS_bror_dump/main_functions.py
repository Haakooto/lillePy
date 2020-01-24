from interpreter_bror import *
if __name__ == '__main__':
    from custom_functions import *
import numpy as np

class add(parentFunctions):
    # because iwant to add stuff
    def __init__(self, *passed):

        self.function_name = "add"
        self.passed = listed_nest_remover(list(passed))
        for i, obj in enumerate(passed):
            if obj == 'x':
                obj = Variable('x')
                self.passed[i] = obj
            if isinstance(obj, add):
                self.passed = add(self.passed + obj.passed).passed#[0]
        for i, obj in enumerate(self.passed):
            if isinstance(obj, add):
                del self.passed[i]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None

    def __call__(self, *args):
        # for now only one variable is allowed
        if len(args) == 1:
            arg = args[0]

            if isinstance(arg, Variable):
                pass
            elif isinstance(arg, numbers.Number):
                sum = 0
                for obj in self.passed:
                    if isinstance(obj, parentFunctions):
                        sum += obj(arg)
                    if isinstance(obj, numbers.Number):
                        sum += obj
                    elif isinstance(obj, Variable):
                        sum += arg
                return sum



class sub(parentFunctions):
    # because iwant to sub stuff
    def __init__(self, *passed):

        self.function_name = "sub"
        self.passed = listed_nest_remover(list(passed))
        for i, obj in enumerate(passed):
            if obj == 'x':
                obj = Variable('x')
                self.passed[i] = obj
            if isinstance(obj, sub):
                self.passed = sub(self.passed + obj.passed).passed
        for i, obj in enumerate(self.passed):
            if isinstance(obj, sub):
                del self.passed[i]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None

    def __call__(self, *args):
        # for now only one variable is allowed
        if len(args) == 1:
            arg = args[0]

            if isinstance(arg, Variable):
                pass
            elif isinstance(arg, numbers.Number):
                sum = 0
                for obj in self.passed:
                    if isinstance(obj, parentFunctions):
                        sum -= obj(arg)
                    if isinstance(obj, numbers.Number):
                        sum -= obj
                    elif isinstance(obj, Variable):
                        sum -= arg
                return sum



class mul(parentFunctions):
    def __init__(self, *passed):
        self.function_name = "mul"
        self.passed = listed_nest_remover(list(passed))
        for i, obj in enumerate(passed):
            if obj == 'x':
                obj = Variable('x')
                self.passed[i] = obj
            if isinstance(obj, mul):
                self.passed = mul(self.passed + obj.passed).passed#[0]
        for i, obj in enumerate(self.passed):
            if isinstance(obj, mul):
                del self.passed[i]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None

    def __call__(self, *args):
        # for now only one variable is allowed
        if len(args) == 1:
            arg = args[0]

            if isinstance(arg, Variable):
                pass
            elif isinstance(arg, numbers.Number):
                prod = 1
                for obj in self.passed:
                    if isinstance(obj, parentFunctions):
                       prod *= obj(arg)
                    if isinstance(obj, numbers.Number):
                        prod *= obj
                    elif isinstance(obj, Variable):
                        prod *= arg
                return prod



class div(parentFunctions):
    def __init__(self, *passed):
        self.function_name = "div"
        self.passed = listed_nest_remover(list(passed))
        for i, obj in enumerate(passed):
            if obj == 'x':
                obj = Variable('x')
                self.passed[i] = obj
            if isinstance(obj, div):
                self.passed = div(self.passed + obj.passed).passed#[0]
        for i, obj in enumerate(self.passed):
            if isinstance(obj, div):
                del self.passed[i]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None
        '''If something goes wrong here, try to enable the below commment'''
        #self(1)
    def __call__(self, *args):
        # for now only one variable is allowed
        if len(args) == 1:
            arg = args[0]

            if isinstance(arg, numbers.Number):
                res = 1
                try:
                    for i,obj in enumerate(self.passed):
                        if isinstance(obj, parentFunctions):
                            res *= obj(arg)**((-1)**i)

                        if isinstance(obj, numbers.Number):
                            res *= (obj)**((-1)**i)

                        elif isinstance(obj, Variable):
                            res *= (arg)**((-1)**i)
                except ZeroDivisionError:
                    print('Error, division by zero')
                    return None
                return res


class cos(parentFunctions):
    def __init__(self, *args):
        self.function_name = 'cos'
        assert len(args) == 1, 'cos() takes only one argument. %i given.' %len(args)
        self.passed = args[0]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None
        self.call_exact = True # decides wheter function will print 3.1415 instead of pi




    def __call__(self, *args):
        if len(args) == 1:
            arg = args[0]
            res = None

            if isinstance(self.passed, parentFunctions):
                res = np.cos(self.passed(arg))
            elif isinstance(self.passed, numbers.Number) or isinstance(self.passed, Variable):
                res = np.cos(arg)
            return res


class sin(parentFunctions):
    def __init__(self, *args):
        self.function_name = 'sin'
        assert len(args) == 1, 'sin() takes only one argument. %i given.' %len(args)
        self.passed = args[0]
        # this will check if the function is actually a function or just a number,
        # i.e cos(x) vs cos(2)
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None
        self.call_exact = True


    def __call__(self, *args):

        if len(args) == 1:
            arg = args[0]
            res = None

            if isinstance(self.passed, parentFunctions):
                res = np.sin(self.passed(arg))
            elif isinstance(self.passed, numbers.Number) or isinstance(self.passed, Variable):
                res = np.sin(arg)
            return res

class ln(parentFunctions):
    def __init__(self, *args):
        self.function_name = 'ln'
        assert len(args) ==1, 'ln() takes only one argument. &i given' &len(args)
        self.passed = args[0]
        if isinstance(self.passed, Variable):
            self.variable = self.passed
        else:
            self.variable = None
        self.call_exact = True


    def __call__(self, *args):
        if len(args) == 1:
            arg = args[0]
            res = None

            if isinstance(self.passed, parentFunctions):
                res = np.log(self.passed(arg))
            elif isinstance(self.passed, numbers.Number) or isinstance(self.passed, Variable):
                res = np.log(arg)
            return res



if __name__ == '__main__':
    x = Variable('x')

    obj = sin(ln(2))
    print(obj)
