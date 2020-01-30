from interpreter_bror import *

if __name__ == "__main__":
    from custom_functions import *
    from numbers import Number
    import sys
import numpy as np


class Variable:
    def __init__(self, name="x"):
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

        if len(args) == 1:
            try:
                assert (len(args[0])) > 1, '"add" takes more than 1 argument! [2]'
            except:
                pass
        else:
            assert len(args) > 1, '"add" takes more than 1 argument!'

        # we create several attributes for later
        self.init_args = list(args)
        self.str_args = None
        self.call_arg = None

    def __str__(self, *args):
        if debug:
            print("__str__ called")

        """
        The following if-statement is only true if __str__ is called at the same
        time as the instance is being created. i.e print(add(1,2)).
        """
        self.str_args = args
        if self.str_args == ():
            resnumb = 0
            resvar = ""
            try:
                if len(self.init_args[0]) > 1:
                    temp_init_args = self.init_args[0]
            except:
                temp_init_args = self.init_args
            for index, obj in enumerate(temp_init_args):
                if isinstance(obj, parentFunction):
                    if debug:
                        print("__str__ parentFunction")
                    if isinstance(obj, add):
                        if obj == self:
                            print("equal")
                        del temp_init_args[index]
                        self.init_args = temp_init_args
                        return str(
                            add(listed_nest_remover(obj.init_args + self.init_args))
                        )

                elif isinstance(obj, numbers.Number):
                    resnumb += obj

                elif isinstance(obj, Variable):
                    if resvar == "+x":
                        resvar = "+2*x"
                    elif resvar == "":
                        resvar = "+x"
                    else:
                        resvar = "+" + str(int(resvar[1]) + 1) + "x"

            return str(resnumb) + resvar

        # This will only be true when __str__ is called explicitly via the __call__ method
        elif self.str_args != ():
            pass

    def __call__(self, *args):
        if debug:
            print("__call__ called")

        self.call_arg = args[0]

        """!CURRENTLY DISABLED!
           we check if there is a variable in the init_args and if so, any attempt at
           calling the function will return an error, as you should not be able to call numbers"""
        if not (True in [isinstance(obj, Variable) for obj in self.init_args]):
            pass  # print('Error! Cannot call a number as a function of variable!')
            # sys.exit(1)

        # If the call argument is a variable, the the normal function will be called'''
        if isinstance(self.call_arg, Variable):
            return self

        # if the called argument is a number then the valued function (add) will return '''
        elif isinstance(self.call_arg, numbers.Number):
            """init_args_dummy is equal to self.init_args,
                except all variables are replaced by the called number"""
            init_args_dummy = [
                self.call_arg if isinstance(obj, Variable) else obj
                for obj in self.init_args
            ]
            res = 0
            for obj in init_args_dummy:
                if isinstance(obj, (numbers.Number, np.ndarray)):
                    # if the object is a number, we simply add it to the result
                    res += obj
                elif isinstance(obj, parentFunction):
                    # if the object is another function, we add its
                    # functional value at teh call argument
                    res += obj(self.call_arg)
            return res

        # if the called argument is another function, the function will be called first'''
        elif isinstance(self.call_arg, parentFunction):
            if self.call_arg == self:
                # This is a bugfix that fixes tha issue of a function not being able to be called by itself
                self.call_arg = add(self.call_arg.init_args)
            if debug:
                print("is parentFunction")
            # first we check if the call_arg function is being called with
            # expressivly n\mention of variable or not. either way is fine.
            # i.e f instead of f(x)

            try:
                if isinstance(self.call_arg.call_arg, Variable) or (
                    self.call_arg.call_arg is None
                ):
                    # this will succeed if f or f(x) is called.
                    new_init_args = [
                        self.call_arg if isinstance(obj, Variable) else obj
                        for obj in self.init_args
                    ]
                    return add(new_init_args)
                    # return add(self,self.call_arg)
                # elif isinstance(self.call_arg.call_arg, numbers.Number):
                #    print(self.call_arg.call_arg)
            except:
                if debug:
                    print("FAULIRE")
                pass

    def copy(self):
        return add(self.init_args)


debug = False


x = Variable()
a = add(1, x)
b = add(2, x)
g = add(3, x)

print(g)
print(g(1))

y = np.arange(5)
z = np.arange(5)

h = str(g)
print(h)

print(g(y))

print(y + z)
X = add(y, z, x)
print(X(1))

# bugs:
"""
DONE recursive adding of same function returns None
DONE adding called functions (called with number) does not remove the x from higher funtions: print(add(2,a(add(1,x))))
'''

## TODO:
'''
legg til pow-classe slik at multiplikasjon funker utenom string
'''
"""
