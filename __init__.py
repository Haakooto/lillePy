from . import function
from . import stringHandling
from .function import *
from .stringHandling import *
import CallableModules


global x
x = Variable("x")


def __call__(*args, **kwargs):
    return args[0]


CallableModules.patch()
