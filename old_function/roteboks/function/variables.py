import numpy as np


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
        S = "\nVariables decleared in function:\n"
        for i in self.vars:
            S += f"{i}: {self(i)}\n"
        return S
