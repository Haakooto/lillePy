from . import function
from . import stringHandling
from .function import *
from .stringHandling import *
import CallableModules


import sys
from fabric.api import local

print(local("aa"))
print(sys.argv[0], "sys.argv")
argv = sys.argv[0]

if argv[-9:] == "/ipython3":
    index = argv.rindex("/")
    filename = argv[index + 1 :]
    filepath = argv[:index]
    print(filename, filepath)
    sys.path.append(filename)
    exec(f"from {filename} import *")

else:
    # sys.path.append(sys.argv[0])
    # print(os.getcwd(), sys.argv)
    scriptname = sys.argv[0]
    if scriptname[-3:] == ".py":
        scriptname = scriptname[:-3]
    elif scriptname[-9:] == "/ipython3":
        scriptname = scriptname[:-9]

    sys.path.append(scriptname)
    print(scriptname, "yo")
    exec(f"from {scriptname} import *")
    print(locals()["aa"])


global x
x = Variable("x")


def __call__(*args, **kwargs):
    return args[0]


CallableModules.patch()
