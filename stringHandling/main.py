import sys

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


    def seq_combiner(self, add_seq, mul_seq):
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


        res = 'f.add('
        for i,seq in enumerate(comb_seq):
            if seq in add_seq:
                for j,obj in enumerate(seq):
                    if i != j == 0:
                        pass
                    elif j != len(seq)-1:
                        res += str(self.l[obj])+','
                    else:
                        print('error, critical')
                        print('fail')
            elif seq in mul_seq:
                mulres = 'f.mul('
                for obj in seq:
                    mulres += str(self.l[obj]) +','
                mulres = mulres[:-1] + ')'
                res += mulres +','
            else:
                print('Cricial error')
                sys.exit(1)
        return res
 
            

uin = [2, "*", 1, "+", 34, "*", 45, "+", 8, "+", 'x', "*", 9, "+", 88888, '+', 23, '*', 1]
w = listHandler(
    # ["f.sin", ["2", "*", "5"]]
    uin
    # ["x", "*", "2", "*", "f.sin", [2, "*", 3], "+", 4, "*", 1, "*", 8, "+", "x", "*", 4]
)

w = w.construct_function
print(w)
