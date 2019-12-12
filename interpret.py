import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

class CAS:
    def __init__(self, expression):
        self.original = str(expression)
        self.func = []
        self._interpret(self.original)

    def __repr__(self):
        pass

    def __call__(self, x):
        pass

    def __str__(self):
        return self.original

    def _chr_to_str(self, chr):
        if chr == "+":
            return "add"
        elif chr == "-":
            return "sub"
        elif chr == "*":
            return "mul"
        elif chr == "/":
            return "div"

    def _interpret(self, expr):
        term = []
        parenthesis = 0
        idx = -1

        for char in expr:
            idx += 1
            if char == "(":
                parenthesis += 1
                continue
            elif char == ")":
                parenthesis -= 1
                continue
            if char == ("+" or "-") and parenthesis == 0:
                operator = 
                term[self._chr_to_str(char)] = self._interpret(expr[:idx])




def main():
    f = CAS("2x+3")


if __name__ == "__main__":
    main()
