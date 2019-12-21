import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import re


class LAS_func:
    def __init__(self, expression):
        self.original = str(expression)
        self.function = []
        self.variables = {}

        self.interpret(self.original)

    def interpret(self, expr):
        if "=" in expr:
            expr = self._defined_function(expr)

        expr_array = np.asarray([s for s in expr], dtype=str)
        left_paranthesis = np.where(expr_array == "(")
        right_paranthesis = np.where(expr_array == ")")

        self._parenthesis_count(left_paranthesis, right_paranthesis)

        assert left_paranthesis.shape >= right_paranthesis.shape, "Too many "

        # print(expr.find("("))
        for m in re.finditer("(", expr):
            print(m)
        # p = [m.start() for m in re.finditer("(", str(expr))]
        # print(p)
        # expr = np.asarray(expr, dtype=str)
        # print(expr)
        # print(np.where(expr == "2"))

    def _defined_function(self, expr):
        # if user has defined, such as f(x) = something
        # can use this to find main variable(s)
        # for now, just return what's after =
        return expr[expr.find("=") + 1 :]

    def _parenthesis_count(left, right):
        l = len(left)
        r = len(right)
        if l > r:
            self = self.original + ")" * (l - r)
        elif 


def main():
    """
    input: "f(t)=Vp + vmax*sin((2pi/P)(t-t0))"
    output:
        ["add", Vp, ["mul", vmax, [sin, ["mul", ["div", ["mul", 2, pi], P], ["sub", t, t0]]]]]
    """
    f = LAS_func("f(t) = Vp + vmax*sin((2pi/P)(t-t0))")


if __name__ == "__main__":
    main()
