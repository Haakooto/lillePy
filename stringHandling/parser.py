class Parser:
    initKwargs = {"includeAdd": True, "includeMul": True}

    def parse(string, **kwargs):
        """Due to the nature of the dict().get() function returning None
            if the key is nonexistent, """
        if kwargs == {}:
            kwargs = Parser.initKwargs.copy()

        build = Parser.parseAdd(string, includeAdd=kwargs.get("includeAdd"))
        # build = Parser.parseMul(build, includeMul=kwargs.get("includeMul"))
        return build

    def parseAdd(string, **kwargs):
        """this method will replace the elemtens added in a string with a
        lillepy-expression on the form: a+b+c -> lp.Add(a,b,c).
        includeAdd is optional argument of wether the parser should return
        the result with our without the lp.Add( ... ) around the result"""

        includeAdd = kwargs.get("includeAdd")

        string = string.replace(" ", "")

        """First we do a quick check to check if the string actually has any
        sums in its current parenthesis group"""
        parSections = Parser.locateParSections(string)
        searchString = Parser.cutSections(string, parSections)

        if "+" not in searchString:
            includeAdd = False

        build = ""

        addIndices = Parser.locateSymbol(string, "+")
        iterString = iter(enumerate(string))

        for index, obj in iterString:

            if obj == "+":
                build += ","
                continue

            elif obj == "(":
                opening = index

                closing = Parser.locateClosingParenthesis(string, index)

                """if there are no additions in the parenthesis, we of course skip this section.
                However we need to be careful when checking the section for plus signs,
                as any plussigns within another parenthesises will NOT count towards
                deciding wether our surrent parenthesis group has addidion in it"""
                """We separate the string into severalt sections of interest (SOI). these
                sections do not include parenthseis groups of lower order, separators like "," etc."""
                parSections = Parser.locateParSections(string[opening + 1 : closing])
                searchString = Parser.cutSections(
                    string[opening + 1 : closing][:], parSections
                )
                # commaLocations = Parser.locateSymbol(searchString, ",")
                # searchString = list(searchString)
                # for loc in commaLocations:
                #    del searchString[loc]
                # searchString = "".join(searchString)
                # print(f"searchString: {searchString}")
                if "+" not in searchString:
                    build += "("
                    continue

                """next we determine if the par is either a function call or a group.
                    we do this because in some instances,
                    we wish to keep the parenthesis, i.e in sin(2+x)->sin(lp.Add(2,x)),
                    and in some cases, we do no not, i.e (2+3)*8 -> lp.Add(2,3)*8"""
                isFuncGroup = Parser.parIsFunctionGroup(string, index)
                if isFuncGroup:
                    optionalPar = {"L": "(", "R": ")"}
                else:
                    optionalPar = {"L": "", "R": ""}

                # we add to the build
                build += f'{optionalPar["L"]}lp.Add({Parser.parse(string[opening+1:closing], includeAdd=False)}){optionalPar["R"]}'

                """Finally we continue past the parenthesis with the next() function.
                    However, if there are any "," to the r"""

                for foo in range(closing - opening):
                    next(iterString)

            else:
                build += obj
        """We will only add an lp.Add() around the return object if the called parse
            is not a child of any other ongoing parse."""
        if includeAdd:
            return f"lp.Add({build})"
        else:
            return build

    def parseMul(string, **kwargs):
        """parseMul will typically be called AFTER parseAdd, and we therefore need
            to do some extra checks"""

        includeMul = kwargs.get("includeMul")

        build = ""

        string = string.replace(" ", "")

        iterString = iter(enumerate(string))
        for index, obj in iterString:

            if obj == "*":
                build += ","
                continue

            elif obj == "(":

                opening = index
                closing = Parser.locateClosingParenthesis(string, index)

                """If we encounter a par we need to check wether the par is part
                    of a function or a multiplication"""
                isOprGroup = Parser.parIsFunctionGroup(string, index, ["Add", "Sub"])

                if isOprGroup:
                    # if this is the case, we need to stop including objects in our
                    # operator at the first instance of a "," or any other separator

                    build += f"(lp.Mul({Parser.parse(string[opening+1:closing], includeMul=False)}))"
                    separatorIndices = Parser.locateSymbol(
                        string[opening:closing], ",",
                    )
                    for separatorIndex in separatorIndices:
                        pass

            elif obj == ",":
                pass
            else:
                build += obj
        if includeMul:
            return f"lp.Mul({build})"
        else:
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

    def sectionsOfInterest(string, **kwargs):
        """The kwargs will be broken down into separators, groupers and identifiers.
        The section following a separator until another separator is not of interest.
        Groupers consist of two characters that mark the opening and closing of
        a SOI.
        The identifier is what qualifies the group as of interest. As of now there is
        only one type of identifier, and it makes an section of interest
        if it contains that literal identifier"""

        separators = kwargs.get("separators")
        groupers = kwargs.get("groupers")
        identifiers = kwargs.get("identifiers")

        if "()" in groupers:
            # currently only functioning grouper is "()"
            groupedArea = Parser.locateParSections(string)

        searchString = Parser.cutSections(string[:], groupedArea)
        print(string, "|", searchString)
        SOI = []
        foo = ""
        for i, obj in enumerate(searchString):
            if obj in separators:
                print(foo, "foo")
                SOI.append(foo)
                foo = ""
                continue
            foo += obj
            if i == len(searchString) - 1:
                SOI.append(foo)

        searchString = list(searchString)
        for i, section in enumerate(searchString):
            for id in identifiers:
                if id not in section:
                    del searchString[i]

        return SOI


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

foo = "2+(1+(1+23))"
a = "1+2,2+(3+8(+2)),2"
print(Parser.parse(foo))
# print(Parser.parse("lp.Add(1+2(3+8),2)"))
# FEIL: OMrådene blir feil i searchstring
