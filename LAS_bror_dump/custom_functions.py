from interpreter_bror import *
import write_manager as wm
if __name__ == '__main__':
    from main_functions import *

class customFunction(parentFunctions):
    def __init__(self,*passed):
        self.passed = listed_nest_remover(list(passed))
        self.function_name = '|temp|'
        writestring = str(self.passed[0]) +'|'+ self.function_name +'|'
        wm.write_function(writestring, self.function_name)
        self.x = Variable('x')


    def __call__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Variable):
                return self
            else:
                return self.passed[0](arg)


    def write_function(self):
        '''
        formatting: |function name|
        '''
        writestring = str(self.passed[0]) +'|'+ self.function_name +'|'

        wm.write_function(writestring, self.function_name)


    def set_name(self,name):
        wm.rewrite_function_name(self.function_name, name)
        self.function_name = str(name)
        self.function_name_super = str(name)
    def print_def(self):
        print(self.passed[0])



def getfunc(fname):
    return lambda x: eval(wm.get_func(fname))(x)
if __name__ == '__main__':
    x = Variable('x')
    #cot = customFunction(div(cos(x),sin(x)))
    #cot.set_name('cot')
    y = getfunc('newx')
    print(y(1))
