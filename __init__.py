from . import myfunc
from .myfunc import *
import CallableModules


def __call__(*args, **kwargs):
    return args[0]


CallableModules.patch()
