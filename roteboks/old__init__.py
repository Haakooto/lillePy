"""
The order of this program mst not be changed. It has to be as follows:
String handling, make modules callable, import locals from user
"""
from . import function as f
from numbers import Number
import sys


global debug
debug = False
local_user_dict = {}

# ============================================================


"""
String handling.
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
List handling
"""

def remove_break(usr_list):
    res = []
    for i, obj in enumerate(usr_list):
        if type(obj) == list:
            res.append(remove_break(obj))
        elif obj != "BREAK":
            res.append(obj)
    return res


def listify_from_break(usr_list):
    res = []
    for i, obj in enumerate(usr_list[:]):
        if type(obj) == list:
            a = remove_break(obj)
            usr_list[i] = a

    indices = [0] + [i for i, obj in enumerate(usr_list) if obj == "BREAK"]
    for i, index in enumerate(indices):
        if i == 0:
            continue
        elif i == 1:
            res.append(usr_list[indices[i - 1] : index])
        else:
            res.append(usr_list[indices[i - 1] + 1 : index])
    return res


class listHandler:
    operators = ["+", "-", "*", "/"]
    """
    This will convert the list from stringHandler into a lillepy function
    """

    def __init__(self, l):
        self.l = l

    def locate_operator_sequence(self, *args):
        arg = args[0]
        self.operators_excluded = self.operators[:]
        self.operators_excluded.remove(arg)

        # this will locate all the elements to be multiplied/added
        # ['x', '*', 2, '*', 'f.sin', [2, '*', 3], '+', 4, '*', 1, '*', 8]
        # will return [ [0,2,4,[5,[0,2]]], [7,9,11] ]
        # [2, '*', 'x', '*', [1, '+', 'x']]
        # will return [0,2,[4,[]]]
        # [[1, '*', 'x'], '*', 2]
        # will return [[0,[0,2]], 2]
        # ['f.sin', [1, '*', 'x'], '*', 2]
        # will return [0, [1,[0,2]],3]
        # any parenthesis is noted by [index_of_parenthesis, locate_operator_sequence(parenthesis)]

        # this finds the '*' or '+' - indexes. For now only support for written
        # '*' or '+'-signs are included. If we wish to expand the support, this is where
        # to do it.
        indices = [i for i, obj in enumerate(self.l) if obj == arg]
        # print(indices)

        res = []
        for i, index in enumerate(indices):
            prev_obj = self.l[index - 1]
            next_obj = self.l[index + 1]

            # we check if our current mul-sign is the last in a product
            last = False
            if index == indices[-1]:
                last = True
            elif type(self.l[index + 2]) == list:
                if str(self.l[index + 1])[:2] == "f.":
                    if self.l[index + 3] != arg:
                        last = True
            elif self.l[index + 2] != arg:
                last = True

            if type(prev_obj) == list:
                # if the object is a list, we also have to check if the
                # preceeding object is a function
                if index > 1:
                    if str(self.l[index - 2])[:2] == "f.":
                        res.append(index - 2)
                # either way we add the parenthesis
                res.append(
                    [index - 1, listHandler(prev_obj).locate_operator_sequence(arg)]
                )

            elif prev_obj not in self.operators_excluded:
                res.append(index - 1)
            if last:
                if str(next_obj)[:2] == "f.":
                    res.append(index + 1)
                    res.append(
                        [
                            index + 2,
                            listHandler(self.l[index + 2]).locate_operator_sequence(
                                arg
                            ),
                        ]
                    )
                elif type(next_obj) == list:
                    res.append(
                        [index + 1, listHandler(next_obj).locate_operator_sequence(arg)]
                    )

                else:
                    res.append(index + 1)
                res.append("BREAK")
        return res


    def seq_combiner(self, add_seq, mul_seq):
        if mul_seq == []:
            return add_seq
        elif add_seq == []:
            return mul_seq
        # this takes inn two sequences of types mul and add
        # and sorts dem numerically. i.e an input of
        # mul_seq = [[4, 6], [10, 12], [16, 18]]
        # add_Seq = [[0, 2, 4], [6, 8, 10], [12, 14, 16]]
        # yields [[0, 2, 4], [4, 6], [6, 8, 10], [10, 12], [12, 14, 16], [16, 18]]
        add_seq, mul_seq = add_seq[:], mul_seq[:]
        switch = {'add_seq':'mul_seq', 'mul_seq':'add_seq'}
        curr_seq = 'mul_seq'
        if add_seq[0][0] < mul_seq[0][0]:
            curr_seq = 'add_seq'
        res = []
        while True:
            res.append(eval(curr_seq)[0])
            eval(curr_seq).pop(0)
            curr_seq = switch[curr_seq]
            if len(add_seq) == len(mul_seq) == 0:
                break
        return res




    @property
    def construct_function(self):
        mul_seq = listify_from_break(self.locate_operator_sequence("*"))
        add_seq = listify_from_break(self.locate_operator_sequence("+"))
        comb_seq = self.seq_combiner(add_seq,mul_seq)


        if len(comb_seq) > 1:
            res = 'f.add('
        else:
            res = ''
        print(res, "this is the res before first for loop")
        for i,seq in enumerate(comb_seq):
            if seq in add_seq:
                for j,obj in enumerate(seq):
                    if i != j == 0:
                        continue
                    elif (j != len(seq)-1) or i == len(comb_seq)-1:
                        res += str(self.l[obj])+','
                        print(res, "Heeeeeellllllloooooo")
                    else:
                        print("wat3")
                        continue
                print(res, "res")
            elif seq in mul_seq:
                mulres = 'f.mul('
                for obj in seq:
                    mulres += str(self.l[obj]) +','
                mulres = mulres[:-1] + ')'
                res += mulres +','
            else:
                print('Cricial error')
                sys.exit(1)
        if len(comb_seq) > 1:
            res = res[:-1] + ')'
        else:
            res = res[:-1]
        print(res, "falalalalalalalalalla")
        return res


# ============================================================
"""
Make module callable with other module 'CallableModules'
"""


class lillepy:
    __name__ = "lillepy"

    def __call__(self, *args):
        if failsafe == 1:
            x = f.Variable("x")
            uin = args[0]
            w = stringHandler(uin)
            split = w.splitted_list()
            print(split)
            w = listHandler(split).construct_function
            print(w)
            return eval(w)


sys.modules[__name__] = lillepy()

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
