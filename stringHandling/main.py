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

    def find_mul_seq(self, index):
        i = index
        il = [index - 1]
        while True:
            obj = self.l[i]
            if obj == "*":
                i += 1
            elif obj[:2] == "f.":
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
        for i in indexes:
            res += str(self.l[i]) + ","
        return res + ")"

    def list_to_expr(self):
        i = 0
        lc = self.l[:]
        while True:
            obj = self.l[i]
            print(obj)
            if type(obj) == list:
                dummy_instance = listComprehension(obj)
                res = dummy_instance.list_to_expr()
                print(res, "a")
                lc[i] = res
                i += 1
            elif obj == "*":
                res = self.find_mul_seq(i)
                lc = lc[: res[0]] + lc[res[-1] :]

                lc[res[0]] = self.mulform(res)
                i += res[-1] - i - len(self.l[res[0] : res[-1]])
            elif obj in ["+", "-"]:
                i += 1
            elif isinstance(obj, Number):
                i += 1
            if i == len(lc):
                break
        return lc


uin = [23, "*", "f.sin", [2], "*", "f.cos", [1]]


a = listComprehension(uin)
print(a.list_to_expr())
