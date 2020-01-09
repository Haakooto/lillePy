import numpy as np

from .variables import Variables
from .interpreter import Interpreter


class LAS:
    def __init__(self, expression):
        if not isinstance(expression, str):
            raise TypeError(
                f"given expression must be 'str', not '{type(expression)}''"
            )

        self.original = expression
        self.expression = [s for s in expression]
        self.vars = Variables()

        self.haupt = lambda: self.there(
            np.asarray(
                [
                    list(self.vars.vars.keys())[-i - 1]
                    if list(self.vars.vars.values())[-i - 1]() is None
                    else None
                    for i in range(len(self.vars.vars))
                ]
            )
        )[0]

        self.Interpreted = Interpreter(self, self.original)

    @staticmethod
    def there(f):
        return f[np.where(f)]

    def decleare_variables(self, vars):
        self._add_variables(vars)

    def set_variable(self, name, value):
        self.vars.insert(name, value)

    def unset_variable(self, name):
        self.vars.insert(name, None)

    def _add_variables(self, vars):
        if isinstance(vars, dict):
            for key, value in vars.items():
                self.vars.insert(key, value)

        elif isinstance(vars, (list, tuple, np.ndarray)):
            for var in vars:
                self.vars.insert(var, None)

        elif isinstance(vars, str):
            vars = vars.split(", ")
            for var in vars:
                self.vars.insert(var, None)

        elif isinstance(vars, (int, float)):
            raise TypeError("Variable names must be str")


def main():
    pass


if __name__ == "__main__":
    main()
