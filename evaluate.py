import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time


operations = ["add", "sub", "sum", "mul", "pow"]
funcs = ["sin", "cos", "exp"]
passables = ["var", "fint", "param", "const"]


class OP:
    def add(inp):
        typ1 = inp[0][0]
        typ2 = inp[1][0]
        if typ1 in passables:
            first = inp[0][1]
        else:
            first = eval(f"OP.{typ1}(inp[0][1])")

        if typ2 in passables:
            second = inp[1][1]
        else:
            second = eval(f"OP.{typ2}(inp[1][1])")

        return first + second


def main():
    pass


if __name__ == "__main__":
    main()
