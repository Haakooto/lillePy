from . import function
from . import stringHandling
from .function import *
from .stringHandling import *
import CallableModules


import sys
import os

sys.path.append(sys.argv[0])
print(os.getcwd(), sys.argv[0])
scriptname = sys.argv[0]
if scriptname[-3:] == ".py":
    scriptname = scriptname[:-3]
print(scriptname)
exec(f"from {scriptname} import *")
print(locals()["aa"])


global x
x = Variable("x")


def __call__(*args, **kwargs):
    return args[0]


CallableModules.patch()
