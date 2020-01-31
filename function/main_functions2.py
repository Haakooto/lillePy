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
    def __init__(self, functionName):
        self.functionName = functionName

        self.function_dict = {"add": add, "sin": sin}
        self.function_class = eval(functionName)

    def __call__(self, *args):
        if debug:
            print("parentFunction __call__ called")
        self.call_arg = args[0]

        # If the call argument is a variable it will jsut return the function itself
        if isinstance(self.call_arg, Variable):
            if debug:
                print("parentFunction variable")
            return self

        # If the call argument is a number, the mathematical function will be called
        elif isinstance(self.call_arg, numbers.Number):
            if debug:
                print("parentFunction number")
            # init_args_variable_replaced is the same as sellf.init_args except all
            # the variables has been replaced by the called numerical value
            init_args_variable_replaced = [
                self.call_arg if isinstance(obj, Variable) else obj
                for obj in self.init_args
            ]
            # each function has a different call method, i.e add adds values and
            # cos takes the cosine of a single value. In this dictionary the
            # respectable call functions are called and returned as the final value

            return self.function_class.function_call(self, init_args_variable_replaced)
            # self.function_dict[self.functionName].function_call(
            #    self, init_args_variable_replaced
            # )

        # If the call argument is a function, the wollfwin is true
        elif isinstance(self.call_arg, parentFunction):
            if debug:
                print("parentFunction parentFunction")
            if self.call_arg == self:
                # This is a bugfix that fixes tha issue of a function not being able to be called by itself
                self.call_arg = self.function_class(self.call_arg.init_args)
                # self.function_dict[self.functionName](
                # self.call_arg.init_args
                # )

            # first we check if the call_arg function is being called with
            # expressivly n\mention of variable or not. either way is fine.
            # i.e f instead of f(x)

            # The expression in the try would normally fail if the call_arg had
            # no call_arg of its own
            try:
                if isinstance(self.call_arg.call_arg, Variable) or (
                    self.call_arg.call_arg is None
                ):
                    # this will succeed if f or f(x) is called.
                    new_init_args = [
                        self.call_arg if isinstance(obj, Variable) else obj
                        for obj in self.init_args
                    ]
                    return self.function_class(new_init_args)
                    # self.function_dict[self.functionName](new_init_args)

            except:
                if debug:
                    print("FAILURE")
                pass

    def __str__(self, *args):
        if debug:
            print("parentFunction __str__ called")
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

            return self.function_class.function_str(
                self, temp_init_args, call_exact=False
            )  # self.function_dict[self.functionName].function_str(
            # self, temp_init_args, call_exact=False
            # )
        else:
            print("Hello")

    def copy(self):
        return self.function_class(self.init_args)


class add(parentFunction):
    def __init__(self, *args):
        super().__init__("add")
        if len(args) == 1:
            try:
                assert (len(args[0])) > 1, '"add" takes more than 1 argument! [2]'
            except:
                pass
        else:
            assert len(args) > 1, '"add" takes more than 1 argument!'

        # we create several varaibles for later
        self.init_args_initial = list(args)
        self.str_args = None
        self.call_arg = None
        self.init_args = self.init_args_initial
        """REMEMBER TO REMVOE THE ABOVE!!!"""
        # here we try to compact some expressions. i.e make sin(x)+sin(x)->2*sin(x)

        class custom_dictionary(dict):
            def __init__(self):
                self = dict()

            def add(self, key, value):
                self[key] = value

        no_of_same_func_dict = custom_dictionary()

        for i, obj in enumerate(args):
            if isinstance(obj, parentFunction):
                # if the argument is a function, we check if there are any otehr examples
                # of argumants that are a) the same function or b) has the same principle
                # init arguments

                if obj in args[i:]:
                    dummy = 1
                    for obj2 in args[i:]:
                        dummy += 1
                        no_of_same_func_dict.add(str(obj), dummy)

                for j in range(i, len(args)):
                    # check if the same identical function is present:
                    pass
        # print(no_of_same_func_dict)

    def __stre__(self, *args):
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

    def __calle__(self, *args):
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
                if isinstance(obj, numbers.Number):
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
                    print("FAILURE")
                pass

    def function_call(self, *args):
        # this is a manual function call by the parentFunction in the __call__ method.
        res = 0

        init_args_variable_replaced = args[0]
        for obj in init_args_variable_replaced:
            if isinstance(obj, numbers.Number):
                # if the object is a number, we simply add it to the result
                res += obj
            elif isinstance(obj, parentFunction):
                # if the object is another function, we add its
                # functional value at teh call argument
                res += obj(self.call_arg)
        return res

    def function_str(self, *args, call_exact=False):
        # the manual str called from parent __str__
        resnumb = 0
        resvar = ""
        resfunc = ""
        init_args = args[0]
        for index, obj in enumerate(init_args):

            if isinstance(obj, parentFunction):

                if debug:
                    print("__str__ add ")
                if isinstance(obj, add):
                    del init_args[index]
                    self.init_args = init_args
                    return str(add(listed_nest_remover(obj.init_args + self.init_args)))

                else:

                    # this will call if the called element is a function of not type add

                    # this temp variable is to check if the called function is a number or
                    # undetermined function
                    temp_resfunc = str(obj(obj.init_args[0]))

                    try:
                        # the float call will fail if temp_resfunc is not a string of a number
                        resnumb += float(temp_resfunc)

                    except:
                        try:
                            resfunc += "+" + str(obj(obj.init_args[0]))
                        except:
                            resfunc += "+" + str(obj)

            elif isinstance(obj, numbers.Number):
                resnumb += obj

            elif isinstance(obj, Variable):
                if resvar == "+x":
                    resvar = "+2*x"
                elif resvar == "":
                    resvar = "+x"
                else:
                    print("resvar")
                    print(resvar[1])
                    resvar = "+" + str(int(resvar[1]) + 1) + "*x"
        if resnumb == 0:
            resnumb = ""
            resvar = resvar[1:]
            resfunc = resfunc[1:]

        return str(resnumb) + resvar + resfunc


class sub(parentFunction):
    def __init__(self, *args):
        super().__init__("sub")
        if len(args) == 1:
            try:
                assert (len(args[0])) > 1, '"sub" takes 2 or more argument! [2]'
            except:
                pass
        else:
            assert len(args) > 1, '"sub" takes 2 or more argument!'

        # we create several varaibles for later
        self.init_args = list(args)
        self.str_args = None
        self.call_arg = None

    def __str__(self, *args):
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


class mul(parentFunction):
    def __init__(self, *args):
        super().__init__("mul")
        self.init_args = list(args)
        self.str_args = None
        self.call_arg = None

    def function_call(self, *args):
        args = args[0]
        numres = 1
        for i, obj in enumerate(args):

            if isinstance(obj, numbers.Number):
                numres *= obj
            elif isinstance(obj, parentFunction):
                numres *= obj(self.call_arg)
        return numres

    def function_str(self, *args, call_exact=False):
        # the manual str called from parent __str__
        resnumb = 1
        resvar = ""
        resfunc = ""
        init_args = args[0]
        for index, obj in enumerate(init_args):

            if isinstance(obj, parentFunction):

                if debug:
                    print("__str__ mul ")
                if isinstance(obj, mul):
                    del init_args[index]
                    self.init_args = init_args
                    return str(mul(listed_nest_remover(obj.init_args + self.init_args)))

                else:

                    # this will call if the called element is a function of not type mul

                    # this temp variable is to check if the called function is a number or
                    # undetermined function
                    temp_resfunc = str(obj(obj.init_args[0]))

                    try:
                        # the float call will fail if temp_resfunc is not a string of a number
                        resnumb *= float(temp_resfunc)

                    except:
                        try:
                            resfunc += "*" + str(obj(obj.init_args[0]))
                        except:
                            resfunc += "*" + str(obj)

            elif isinstance(obj, numbers.Number):
                resnumb *= obj

            elif isinstance(obj, Variable):
                if resvar == "*x":
                    resvar = "*x^2"
                elif resvar == "":
                    resvar = "*x"
                else:
                    resvar = "*x^" + str(int(resvar[3]) + 1)  # + "*x"
        if resnumb == 1:
            resnumb = ""
            resvar = resvar[1:]

        return str(resnumb) + resvar + resfunc


class sin(parentFunction):
    def __init__(self, *args):
        super().__init__("sin")
        self.init_args = list(args)
        self.str_args = None
        self.call_arg = None

    def function_call(self, *args):
        arg = args[0][0]
        if isinstance(arg, numbers.Number):

            return np.sin(arg)
        elif isinstance(arg, parentFunction):
            return np.sin(arg(self.call_arg))

    def function_str(self, *args, call_exact=False):
        arg = args[0][0]

        if isinstance(arg, Variable):
            return "sin(x)"
        elif call_exact:
            return "sin(" + str(arg) + ")"
        return self(arg)


class cos(parentFunction):
    def __init__(self, *args):
        super().__init__("cos")
        self.init_args = list(args)
        self.str_args = None
        self.call_arg = None

    def function_call(self, *args):
        arg = args[0][0]
        if isinstance(arg, numbers.Number):

            return np.cos(arg)
        elif isinstance(arg, parentFunction):
            return np.cos(arg(self.call_arg))

    def function_str(self, *args, call_exact=False):
        arg = args[0][0]

        if isinstance(arg, Variable):
            return "cos(x)"
        elif call_exact:
            return "cos(" + str(arg) + ")"
        return self(arg)


debug = False

if __name__ == "__main__":

    x = Variable()
    a = add(2, 2, x, x)
    b = mul(x, 3)
    c = add(mul(x, x), mul(3, 2), x, x, mul(4, x, x, x))
    # c = mul(3,x)
    # print(c)
    a = add(1, x)
    print(add(2, a(add(1, x))))
    # print(b(a(c)))
# bugs:
"""
DONE recursive adding of same function returns None
DONE adding called functions (called with number) does not remove the x from higher funtions: print(add(2,a(add(1,x))))
'''

## TODO:
'''
legg til pow-classe slik at multiplikasjon funker utenom string
legg til sånn at sin(x) + sin(x) -> mul(2,sin(x)) i add
'''
"""
