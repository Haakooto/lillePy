class Parser:
    initKwargs = {"includeAdd": True, "includeMul": True}
    oprSymbolDict = {"+": "Add", "*": "Mul"}

    def parse(string, **kwargs):
        """Due to the nature of the dict().get() function returning None
            if the key is nonexistent, """
        if kwargs == {}:
            kwargs = Parser.initKwargs.copy()

        build = string
        for oprSymb, opr in Parser.oprSymbolDict.items():
            build = Parser.parseOpr(
                build, opr=oprSymb, includeOpr=kwargs.get(f"include{opr}")
            )

        return build

    def parseOpr(string, **kwargs):

        opr = kwargs.get("opr")
        """this method will replace the elemtens added in a string with a
        lillepy-expression on the form: a+b+c -> lp.Add(a,b,c).
        includeAdd is optional argument of wether the parser should return
        the result with our without the lp.Add( ... ) around the result"""

        includeOpr = kwargs.get("includeOpr")
        string = string.replace(" ", "")

        build = ""

        parSections = Parser.locateParSections(string)
        searchString = Parser.cutSections(string, parSections)

        if opr not in searchString:
            includeOpr = False

        oprIndices = Parser.locateSymbol(string, opr)
        iterString = iter(enumerate(string))

        for index, obj in iterString:

            if obj == "(":
                opening = index
                closing = Parser.locateClosingParenthesis(string, index)

                """next we determine if the par is either a function call or a group.
                    we do this because in some instances,
                    we wish to keep the parenthesis, i.e in sin(2+x)->sin(lp.Add(2,x)),
                    and in some cases, we do no not, i.e (2+3)*8 -> lp.Add(2,3)*8"""
                isFuncGroup = Parser.parIsFunctionGroup(string, index)
                """If it is a function ,we need to account for the ',' and end any operation there,
                    meanwhile including the "," in the original operator"""
                if isFuncGroup:
                    build += "("
                    # callSections are the areas between any ","'s
                    callSections = Parser.locateFunctionCallSections(
                        string[opening : closing + 1], zero=opening
                    )
                    for sec in callSections:
                        stringSection = string[sec[0] : sec[-1] + 1]
                        parSections = Parser.locateParSections(stringSection)
                        searchString = Parser.cutSections(stringSection[:], parSections)

                        build += eval(
                            f'Parser.parse(stringSection, include{Parser.oprSymbolDict[opr]} = {opr in searchString}) + ","'
                        )

                        for k in range(len(stringSection) + 1):
                            next(iterString)
                    build = build[:-1] + ")"

                if not isFuncGroup:
                    """If the parenthesis is not a function but just any normal parenthesis, we do not need to bother
                        with checking for the commas"""
                    stringSection = string[opening + 1 : closing]
                    build += eval(
                        f"Parser.parse(stringSection, include{Parser.oprSymbolDict[opr]} = True)"
                    )
                    for k in range(len(stringSection) + 1):
                        next(iterString)
            elif obj == opr:
                build += ","
                continue

            else:
                build += obj
        """We will only add an lp.Add() around the return object if the called parse
            is not a child of any other ongoing parse."""
        if includeOpr:
            build = f"lp.{Parser.oprSymbolDict[opr]}({build})"
        return build

    def locateClosingParenthesis(string, index):
        # this function finds the index of the closing parenthesis in a string
        # index is the index of the parenthesis we wish to find
        # its closed counterpart to
        assert string[index] == "(", f'expected symbol "(", got {string[index]}'
        # this is how many '(' are between the current parenthesis and the fisr cllsing parenthesis
        start_par_amount = string[index + 1 : index + string[index:].index(")")].count(
            "("
        )
        j = start_par_amount
        i = 0
        while j >= 0:
            if string[index + 1 + i] == ")":
                j -= 1
            i += 1
        return index + i

    def locateSymbol(string, symbol, start=None, stop=None):
        # locates the indecies of the symbols "symbol" in the string.
        # optional: Between indexes start and stop

        # if no indecies are given for start and stop, we need to manualy pick them
        if start is None:
            start = 0
        if stop is None:
            stop = len(string)

        indicies = []
        for index, obj in enumerate(string[start:stop]):
            if obj == symbol:
                indicies.append(index + start)
        return indicies

    def parIsFunctionGroup(string, index, *args):
        """THIS NEEDS TO BE OPTIMIZED"""
        """OPTIMIZE WITH REGEX"""

        """ index must be the index of the opening parenthesis in a string.
        will return False in cases like 4*(2+3) and 4-(2+x) and
        True in cases like sin(7+2) and log(3+x).
        If args is empty, this method will only check for the names in fNames.
        If args is not empy, it will only check for the arguments within. (must be list)
        """

        global fNames
        # print(string, index, "yo")
        if args != ():
            fNames = args[0]
        fNames += opNames
        # We iterate "backwards" through the string, in order to catch the
        # first instance of a matching function name.
        stringBwd = string[:index][::-1]
        fNamesBwd = sorted(
            [foo[::-1] for foo in fNames], key=len, reverse=True
        )  # fNames with the names backwards sorted by length, decreasing

        for fName in fNamesBwd:
            if stringBwd[: len(fName)] == fName:
                return True
        return False

    def locateParSections(string):
        """This method locates all the closed parenthesis sections withing the string
            and returns them all in a nested list"""
        res = []
        for i, obj in enumerate(string):
            if obj == "(":
                res.append([i, Parser.locateClosingParenthesis(string, i)])
        return res

    def cutSections(string, sections):
        """section is a nested list of lists of length 2 with the indexes of sections to be removed from the string"""
        letterList = list(string)
        for sec in sections:
            del letterList[sec[0] : sec[1] + 1]

        return "".join(letterList)

    def locateFunctionCallSections(string, zero=0):
        """This method locates the indicies of the sections in a called funtion/operator.
            i.e (23,457,sin(2+x)) -> [[1,2],[4,6],[8,15]]
            The input string has to start and end with parenthesis.
            All returned values will be incearsed by the value of 'zero'."""

        parSections = Parser.locateParSections(string[1:-1])
        parSectionsFlattened = [val for sublist in parSections for val in sublist]

        startOfSec = True
        res = []
        foo = []
        iterable = iter(enumerate(string))
        for i, obj in iterable:
            if i == 0:
                continue
            if startOfSec:
                startOfSec = False
                foo.append(i + zero)
            elif i in parSectionsFlattened:
                openIndex = parSectionsFlattened.index(i)
                for k in range(parSectionsFlattened[openIndex + 1] - i + 1):
                    next(iterable)
            elif obj in [",", ")"]:
                foo.append(i - 1 + zero)
                res.append(foo)
                foo = []
                startOfSec = True
        return res


fNames = [
    "sin",
    "cos",
    "tan",
    "log",
    "ln",
    "arcsin",
    "arccos",
    "acos",
    "asin",
]
opNames = ["lp.Add", "lp.Sub", "lp.Mul", "lp.Div"]

print(Parser.parse("sin(2+8*x*sin(1+8*x))"))
