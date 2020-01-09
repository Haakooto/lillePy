import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time


"""
Think now this was a bad idea in general, 
as we want to build funcs as combinatios of know function

Then there shold be no need to parse the list
But we still have it if this thurns out to be usefull later.
"""


operations = ["add", "sub", "mul", "pow"]  # opeartors take two inputs
funcs = ["sin", "cos", "exp"]  # functions take one input
passables = ["var", "fint", "param", "const"]  # passables take zero input,
# but can take more values, in the case of var and params


class OP:
    def evaluate(f):
        val = eval(f"OP.{f[0]}(f[1])")
        return val

    def add(inp):
        """
        Adds two terms

        Know problems:
        only work if types are fint or nor passable
        taking in param a and param a should return 2a
        """
        typ1 = inp[0][0]
        typ2 = inp[1][0]
        if typ1 in passables:
            first = inp[0][1]
        else:
            first = eval(f"OP.{typ1}(inp[0][1])")
            # recursion to evaluate next step in
        if typ2 in passables:
            second = inp[1][1]
        else:
            second = eval(f"OP.{typ2}(inp[1][1])")

        return first + second


def main():
    # f = 1 + 2
    f = ["add", [["fint", 1], ["fint", 2]]]
    a = OP.evaluate(f)
    print(a)


if __name__ == "__main__":
    main()
