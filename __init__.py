from . import myfunc
from .myfunc import *
import CallableModules


global x
x = Variable("x")


def __call__(*args, **kwargs):
    return args[0]


CallableModules.patch()
