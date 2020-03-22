"""
The order of this program mst not be changed. It has to be as follows:
String handling, make modules callable, import locals from user
"""
# import function

# from .function import *

from .stringHandling import *
# from . import function as f

global local_user_dict, debug, failsafe
import sys


debug = False
failsafe = 0
local_user_dict = {}

# ============================================================


"""
String handling
"""


def listToString(l):
    assert type(l) == list, f"expected type list, got {type(l)}"
    l = removeNestings(l)
    res = ""
    for i in l:
        res += str(i)
    return res


def countNestings(l, count=0):
    for i in l:
        if type(i) == list:
            count = countNestings(i, count + 1)
    return count


def removeNestings(nestedList):
    """ Converts a nested list to a flat list """
    flatList = []
    # Iterate over all the elements in given list
    for elem in nestedList:
        # Check if type of element is list
        if isinstance(elem, list):
            # Extend the flat list by adding contents of this element (list)
            flatList.extend(removeNestings(elem))
        else:
            # Append the elemengt to the list
            flatList.append(elem)

    return flatList


def string_is_number(obj):
    try:
        float(obj)
        return True
    except:
        return False


class stringHandler:
    """A comprehensive string handler that will convert a string
        from user input to a function of lillepy-type"""

    function_names = dir(function)
    for deletion in [
        # "Bunch",  # Dont think we use this
        "Number",
        "Struct",
        "Variable",
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__path__",
        "__spec__",
        "add",
        "basicFunctions",
        "np",
        "operatorFunctions",
        "parentFunction",
        "parentOperator",
        "parents",
        "sys"
        # This list needs to be expanded as new structures are added
    ]:
        function_names.remove(deletion)

    def __init__(self, string):
        self.splitted_expression = []
        self.string = string

        if debug:
            print(self.string, "init string print")

    def find_closing_parenthesis(self, index):
        # this function finds the index of the closing parenthesis in a string
        # index is the index of the parenthesis we wish to find
        # its closed counterpart to
        assert (
            self.string[index] == "("
        ), f'expected symbol "(", got {self.string[index]}'

        # this is how many '(' are between the current parenthesis and the fisr cllsing parenthesis
        start_par_amount = self.string[
            index + 1 : index + self.string[index:].index(")")
        ].count("(")
        j = start_par_amount
        i = 0
        while j >= 0:
            if self.string[index + 1 + i] == ")":
                j -= 1
            i += 1
        return index + i

    def number_segment(self, index):
        res = self.string[index]
        obj = res
        i = 1
        while True:
            try:
                obj = self.string[index + i]
            except:
                break
            if (not string_is_number(obj)) and (obj != "."):
                break
            res += obj
            i += 1
        if res.count(".") > 1:
            print(f"Error, check decimal points in {self.string} around index {i}")
            sys.exit(1)
        return res

    def function_segment(self, index):
        par0_index = self.string[index:].index("(") + index

        par1_index = self.find_closing_parenthesis(par0_index)

        if debug:
            print(self.string[par0_index + 1 : par1_index], "part sent into handler")

        dummy_instance = stringHandler(f"{self.string[par0_index + 1 : par1_index]}")

        dummy_instance.splitted_list()
        if debug:
            print(
                dummy_instance.splitted_expression,
                "splitted expression returned from splitting",
            )
        return (
            f"{self.string[index:par0_index]}",
            dummy_instance.splitted_expression,
        )

    def following_segment_is_function(self, index):
        # currently all functions need to use ().
        try:
            par0_index = self.string[index:].index("(") + index

            if self.string[index:par0_index] in self.function_names:
                return True
        except:
            return False

    def following_segment_is_user_local(self, index):
        for key in sorted(local_user_dict.keys(), key=len, reverse=True):
            if (key in self.string[index:]) and (key[0] == self.string[index]):
                return True, key
        else:
            return False, None

    def splitted_list(self):
        if debug:
            print(f"len(string): {len(self.string)}")
        var = "x"
        i = 0
        while True:
            # print(self.string, "routine, string print")
            # co is short for current object
            if debug:
                print(
                    f"routine string[{i}]={self.string[i]}, splitted_expression = {self.splitted_expression}"
                )
            co = self.string[i]
            if co in [var, "+", "-", "/", "*", "÷"]:
                self.splitted_expression.append(co)
                i += 1
            elif string_is_number(co):
                # fo is short for following objects
                if debug:
                    print(co, "string_is_number")
                fo = self.number_segment(i)
                self.splitted_expression.append(eval(fo))
                i += len(fo)

            elif self.following_segment_is_function(i):

                if debug:
                    print(self.string[i], "following_segment_is_function")
                fname, fexpr = self.function_segment(i)
                self.splitted_expression.append(f"f.{fname}")
                self.splitted_expression.append(list(fexpr))
                # we now increase the index i by the length of our total function
                a = len(fname)
                b = len(self.string[i + a : self.find_closing_parenthesis(i + a) + 1])
                i += a + b
            elif self.following_segment_is_user_local(i)[0]:

                if debug:
                    print(f"{self.string[i]} following_segment_is_user_local")
                local = self.following_segment_is_user_local(i)[1]
                self.splitted_expression.append(f"l.{local}")

                i += len(local)

            elif self.string[i] == "(":
                par0_index = i
                par1_index = self.find_closing_parenthesis(i)
                dummy_instance = stringHandler(self.string[par0_index + 1 : par1_index])
                self.splitted_expression.append(dummy_instance.splitted_list())

                i += len(self.string[par0_index : par1_index + 1])

            else:
                print(f"ERROR string[{i}]={self.string[i]}, len: {len(self.string)}")
                break
            if i == len(self.string):
                break
        return self.splitted_expression


# ============================================================
"""
Make module callable with other module 'CallableModules'
"""
import sys


class callable:
    def __call__(self, *args):
        if failsafe == 1:
            x = f.Variable("x")
            uin = args[0]
            w = stringHandler(uin)
            split = w.splitted_list()
            w = listComprehension(split)

            return eval(w.list_to_expr[0])


sys.modules[__name__] = callable()
"""
def __call__(*args, **kwargs):
    if failsafe == 1:
        uin = args[0]
        w = stringHandler(uin)
        split = w.splitted_list()
        return split


CallableModules.patch()
"""
# ============================================================
"""
Importing the users locals. This must be done outside of a function
"""

pre_import_dir = dir()[:]
scriptname = sys.argv[0]
if scriptname[-3:] == ".py":
    scriptname = scriptname[:-3]
else:
    print(
        "Error, could not import locals. Lillepy does not yet support import of locals from any python venv. The module can still be used. Clock based events will no longer occur"
    )
sys.path.append(scriptname)
tmp_file = "tmp_script"


class Reader:
    def __init__(self, scriptname):
        self.usr = scriptname
        self.names = []
        self.lines = []
        self.imports = []

    def read_usr(self):
        with open(f"{self.usr}.py", "r") as usr:
            in_func = False
            in_multiline = False

            for line in usr.readlines():
                line = line[: line.find("#")]
                if in_multiline:
                    if '"""' in line:
                        in_multiline = False
                        line = line[line.find('"""') :]
                    else:
                        continue
                if '"""' in line:
                    in_multiline = True
                    line = line[: line.find('"""')]
                if line[:4] == "def ":
                    self.names.append(line[4 : line.find("(")])
                    in_func = True
                    func = [line]
                    continue
                if not in_func:
                    line = line.strip()
                    if self.valid_line(line):
                        name = line.split("=")[0].strip()
                        self.names.append(name)
                        self.lines.append(line)
                else:
                    if line[:4] in ("    ", "   "):
                        if self.valid_in_func(line):
                            func.append(line)
                    else:
                        self.lines.append(func)
                        in_func = False

    def valid_line(self, line):
        import re

        if "import" in line:
            if "*" in line:
                import time

                print("YOU HAVE COMMITED THE DEADLY SIN OF STAR-IMPORT!")
                time.sleep(1)
                print("Prepare to meet the consequenses!")
                time.sleep(2)
                import os

                print("Shutting down")
                os.system("echo -n '\a';sleep 0.1;" * 20)
                print("Shutdown complete")
                time.sleep(1)
                sys.exit()
            if "from" in line and "as" not in line:
                names = line[line.find("import") + 6 :].split(",")
                for name in names:
                    self.names.append(name.strip())
            elif "as" in line and "from" not in line:
                self.names.append(line[line.find("as") + 3 :].strip())
            elif "as" not in line and "from" not in line:
                self.names.append(line.split(" ")[1].strip())
            self.imports.append(line)
            return False

        if " = " not in line:
            return False
            # requires propper spacing, which shouldnt be a problem for us, but prob will be, as people are lazy
        n, v = line.split("=")
        value = v.strip()
        if "lambda " in value:
            name = line.split("=")[0].strip()
            self.names.append(name)
            self.lines.append(line)
            return False
        if "Variable(" in value:
            return True
        if " lp(" in value:
            return False
        values = re.split("\+|\*|\-|\/", value)
        for expr in values:
            expr = expr.strip()
            try:
                float(expr)
            except ValueError:
                if "." in expr:
                    if expr[: expr.find(".")] in self.imports:
                        return True
                if expr not in self.names:
                    return False
            else:
                return True

    def valid_in_func(self, line):
        #######
        # Should be implemented for proper checks
        #######
        return True

    def write(self, outfile):
        with open(outfile, "w") as our:
            for line in self.imports:
                our.write(f"{line}\n")

            for line in self.lines:
                if isinstance(line, list):
                    for subline in line:
                        our.write(f"{subline}\n")
                else:
                    our.write(f"{line}\n")

    @property
    def delete(self):
        import os

        os.remove(f"{tmp_file}.py")


R = Reader(scriptname)
R.read_usr()
R.write(f"./{tmp_file}.py")

exec(f"import {tmp_file} as USERIMPORT")

uncommon_dir = list(set(pre_import_dir) ^ set(dir(USERIMPORT)))
uncommon_dir = list(set(uncommon_dir) ^ set(pre_import_dir))

for elem in uncommon_dir[:]:
    if elem[:2] == elem[-2:] == "__":
        uncommon_dir.remove(elem)

    try:
        if (eval(f"USERIMPORT.{elem}").__name__) == "lillepy":
            uncommon_dir.remove(elem)
    except:
        pass

local_user_dict = {}
for elem in uncommon_dir:
    evalElem = eval(f"USERIMPORT.{elem}")
    local_user_dict[str(elem)] = evalElem

import os
here = os.getcwd()
with open(f"{here}/dict.txt", "w") as file:
    file.write(str(local_user_dict))

R.delete
failsafe = 1
# ============================================================
