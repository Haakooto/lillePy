from . import function
from .function import *
from . import stringHandling
from .stringHandling import *


class lillepy:
    __name__ = "lillepy"

    def __call__(self, *args):
        foo, bar = Parser.wrapper(args[0])
        for var in bar:
            exec(f"{var} = Variable('{var}')")
        return eval(foo)


sys.modules[__name__] = lillepy()