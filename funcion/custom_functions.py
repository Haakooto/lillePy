from interpreter_bror import *
from main_functions import *
import write_manager as wm
if __name__ == '__main__':
    from main_functions import *

class customFunction(parentFunctions):
    def __init__(self,*passed, name='None'):
        self.function_name = name
        self.passed = listed_nest_remover(list(passed))
        #self.function_name = '|temp|'
        #writestring = str(self.passed[0]) +'|'+ self.function_name +'|'
        #wm.write_function(writestring, self.function_name)
        self.x = Variable('x')
        self.write_function()

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

        self.was_written = wm.write_function(writestring, self.function_name)


    def set_name(self,name):
        return self.write_function(name)
        #wm.rewrite_function_name(name)
        #self.function_name = str(name)
        #self.function_name_super = str(name)
    def print_def(self):
        print(self.passed[0])



def getfunc(fname):
    #print(eval(wm.get_func(fname)))
    return lambda x: eval(wm.get_func(fname))(x)

def delfunc(fname):
    line = wm.line_locator(fname)
    if line is None:
        print('ERROR, No function named "'+str(fname)+'" found')
        return False
    else:
        wm.del_line(line)
        print('Function "'+str(fname)+'" deleted')
        return True


if __name__ == '__main__':
    x = Variable('x')

    cot = customFunction(div(cos(x),sin(x)), name='cot')
    #cot.set_name('cot')
    #y = getfunc('tan')
    #a = y(cos(2))
    print(cot(1))
