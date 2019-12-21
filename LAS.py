import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time


class Variables:
    """
    Class for holding variables in LAS-functions in dict

    keys are name of variable; str
    values are lambda-function with no argument,
        returning value; int, float, ndarray, None
    """

    def __init__(self):
        self.dictionary = {}
        self.vars = self.dictionary

    def insert(self, name, value):
        """ Make sure types are right, then add lambda-funct to dict """
        if not isinstance(name, str):
            raise TypeError(
                f"variable names must be type 'str', not type '{type(name)}'"
            )

        if isinstance(value, list):
            value = np.asarray(value, dtype=float)

        if not isinstance(value, (int, float, np.ndarray)) and value is not None:
            raise TypeError(
                f"variable value must be number(s) or None, not type '{type(name)}'"
            )

        self.vars[name] = lambda: value

    def __call__(self, name):
        """
        Call by (), lambda triggered
        """
        try:
            return self.vars[name]()
        except KeyError:
            f"variable {name} not defined in fuction"

    def __getitem__(self, name):
        """
        Call by [], lambda not triggered
        """
        try:
            return self.vars[name]
        except KeyError:
            f"variable {name} not defined in fuction"

    def __str__(self):
        S = ""
        for i in self.vars:
            S += f"{i}: {self(i)}\n"
        return S


class LAS:
    def __init__(self, expression):
        if not isinstance(expression, str):
            raise TypeError(
                f"given expression must be 'str', not '{type(expression)}''"
            )

        self.original = expression
        self.vars = Variables()

        self.haupts = lambda: np.asarray(
            [
                list(self.vars.vars.items())[-i - 1][0]
                if list(self.vars.vars.items())[-i - 1][1]() is None
                else None
                for i in range(len(self.vars.vars))
            ]
        )
        self.haupt = lambda: self.haupts()[np.where(self.haupts())][0]
        # self.haupt = lambda: np.asarray(
        #     [
        #         list(self.vars.vars.items())[-i - 1][0]
        #         if list(self.vars.vars.items())[-i - 1][1]() is None
        #         else None
        #         for i in range(len(self.vars.vars))
        #     ]
        # )[
        #     np.where(
        #         np.asarray(
        #             [
        #                 list(self.vars.vars.items())[-i - 1][0]
        #                 if list(self.vars.vars.items())[-i - 1][1]() is None
        #                 else None
        #                 for i in range(len(self.vars.vars))
        #             ]
        #         )
        #     )
        # ][
        #     0
        # ]

        self.variables_given = False
        self.interpreted = False

    def decleare_variables(self, vars):
        self._add_variables(vars)
        self.variables_given = True

    def set_variable(self, name, value):
        self.vars.insert(name, value)

    def unset_variable(self, name):
        self.vars.insert(name, None)

    def _add_variables(self, vars):
        if isinstance(vars, dict):
            for key, value in vars.items():
                self.vars.insert(key, value)

        elif isinstance(vars, (list, tuple)):
            for var in vars:
                self.vars.insert(var, None)

        elif isinstance(vars, str):
            vars = vars.split(", ")
            for var in vars:
                self.vars.insert(var, None)

        elif isinstance(vars, (int, float)):
            raise TypeError("Variable names must be str")


def main():
    # L = Variables()
    # L.insert("b", None)
    # print(L("b"))
    # L.insert("b", 14)
    # print(L["b"]())

    F = LAS("ax+b")
    F.decleare_variables({"x": np.arange(3), "y": None, "a": 1, "b": 4})
    print(F.vars)
    print(F.haupt())

    F.decleare_variables("x, y, z")
    print(F.vars)
    print(F.haupt())


if __name__ == "__main__":
    main()
