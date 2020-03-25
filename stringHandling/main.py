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
        print(self.l, "l")
        indices = [i for i, obj in enumerate(self.l) if obj == arg]

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
        print(res, "res")
        return res

    @property
    def construct_function(self):
        mul_seq = listify_from_break(self.locate_operator_sequence("*"))
        add_seq = listify_from_break(self.locate_operator_sequence("+"))
        print(mul_seq, "mul_seq")
        print(add_seq, "add_seq")

        total = []
        for parent_obj in mul_seq:

            if type(parent_obj[0]) == list:
                mulstart = parent_obj[0][0]
            else:
                mulstart = parent_obj[0]
            if type(parent_obj[-1]) == list:
                mulstop = parent_obj[-1][0]
            else:
                mulstop = parent_obj[-1]

            for j, parent_obj in enumerate(mul_seq):
                res = "f.mul("
                for i, obj in enumerate(parent_obj):
                    print(obj, "obj")
                    if type(obj) == list:
                        print(f"{obj} is list")
                        if str(self.l[obj[0]])[:2] == "f.":
                            continue
                        else:
                            print("here", self.l[obj[0] + 1])
                            print("here2", self.l[obj[0]])
                            call_obj = listHandler(
                                self.l[obj[0] + 1]
                            ).construct_function
                            res += f"{call_obj},"
                    elif str(self.l[obj])[:2] == "f.":
                        print(f"obj {obj} is function")
                        call_obj = listHandler(self.l[obj + 1]).construct_function
                        print(call_obj, "call_obj")
                        res += f"{self.l[obj]}({call_obj}),"
                    else:
                        print("object is neither")
                        res += f"{self.l[obj]},"
                total.append(res[:-1] + ")")
            print(total, "total")
            addres = "f.add("
            if len(mul_seq) < len(add_seq):
                mul_seq += [None]
                total += [None]
            for i, (fmul, mulidx, addidx) in enumerate(zip(total, mul_seq, add_seq)):
                print(i, fmul, addidx, mulidx)

            return total
            # print(mulstart, mulstop)


w = listHandler(
    # ["f.sin", ["2", "*", "5"]]
    [2, "*", 1, "+", 34, "*", 45, "+", 8, "+", 24, "*", 9, "+", 88888]
    # ["x", "*", "2", "*", "f.sin", [2, "*", 3], "+", 4, "*", 1, "*", 8, "+", "x", "*", 4]
)
w.construct_function
