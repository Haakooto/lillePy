import function as f
from numbers import Number


def string_is_number(obj):
    try:
        float(obj)
        return True
    except:
        return False


class listComprehension:
    def __init__(self, l):
        self.l = l

    def find_div_seq(self, i):
        if i > 1:
            if self.l[i - 2][:2] == "f.":
                il = [i - 2, i - 1]
        else:
            il = [i - 1]
        return il + [i + 1]

    def find_mul_seq(self, i):
        if i > 1:
            if self.l[i - 2][:2] == "f.":
                il = [i - 2, i - 1]
        else:
            il = [i - 1]

        while True:
            obj = self.l[i]
            if obj == "*":
                i += 1
            elif str(obj)[:2] == "f.":
                il.append(i)
                il.append(i + 1)
                i += 2
            elif type(obj) == list:
                il.append(i)
                i += 1
            elif string_is_number(obj):
                il.append(i)
                i += 1
            if i == len(self.l):
                break
        return il

    def mulform(self, indexes):
        res = "f.mul("
        i = 0
        while True:
            index = indexes[i]
            if str(self.l[index])[:2] == "f.":
                assert (
                    type(self.l[index + 1]) == list
                ), "cirical error. function expression not list"
                dummy_instance = listComprehension(self.l[index + 1])
                fres = dummy_instance.list_to_expr
                res += f"{str(self.l[index])}({str(fres[0])}),"
                i += 2
            else:
                res += f"{str(self.l[index])},"
                i += 1
            if i == len(indexes):
                break
        return res[:-1] + ")"

    @property
    def list_to_expr(self):
        i = 0
        lc = self.l[:]
        while True:
            obj = self.l[i]
            if type(obj) == list:
                if i > 1:
                    if str(self.l[i - 1])[:2] == "f.":
                        i += 2
                        continue
                dummy_instance = listComprehension(obj)
                res = dummy_instance.list_to_expr
                lc[i] = res
                i += 1
            elif str(obj)[:2] == "f.":
                i += 1
            elif obj == "*":
                mul_seq = self.find_mul_seq(i)
                lc = lc[: mul_seq[0]] + lc[mul_seq[-1] :]
                lc[mul_seq[0]] = self.mulform(mul_seq)
                addlen = mul_seq[-1] - i - len(self.l[mul_seq[0] : mul_seq[-1]])
                i += addlen
            elif obj == "/":
                assert i > 0, f"Error in division expression around string index {i}"
                div_seq = self.find_div_seq(i)
                lc = lc[: div_seq[0]] + lc[div_seq[-1] :]
                lc[mul_seq[0]] = self.divform(div_seq)
            elif obj == "x":
                i += 1
            elif obj in ["+", "-"]:
                i += 1
            elif isinstance(obj, Number):
                i += 1
            else:
                print(i, obj, len(lc), lc)
            if i == len(lc):
                break
        assert len(lc) == 1, f"error, len(lc) = {len(lc)}. Should be 1"
        return lc


uin = ["f.cos", [3], "*", "f.sin", [2, "*", 3, "f.cos", [3, "*", 43, "*", 23]]]

a = listComprehension(uin)
k = f.cos(2)
print(eval(a.list_to_expr[0])(1))
