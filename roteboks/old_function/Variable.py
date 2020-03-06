
class Variable:
    def __init__(self, name=""):
        try:
            float(name)
        except ValueError:
            self.name = str(name)
        else:
            print("Invalid variable name given, can not be number")
            sys.exit()

    def __str__(self):
        return self.string(None)

    def string(self, type):
        return self.name
