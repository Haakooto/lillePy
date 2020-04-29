class Parser:
    def parseAdd(string, isChild=False):
        # this method will replace the elemtens added in a string with a
        # lillepy-expression on the form: a+b+c -> lp.Add(a,b,c)

        # isChild has to be set to True when the parseAdd method is called
        # recursively within itself. See comment ~50 lines down

        addIndices = Parser.locateSymbol(string, "+")

        for index, obj in enumerate(string):
            if obj == "(":
                opening = index
                closing = Parser.locateClosingParenthesis(string, index)
                # if there are any +'s in between the parenthesis, we ignore them
                possibleAddIndices = Parser.locateSymbol(string, "+", opening, closing)
                if possibleAddIndices != []:
                    for addIndex in possibleAddIndices:
                        # this is a bodge, but it works
                        try:
                            addIndices.remove(addIndex)
                        except:
                            pass

        # combine the elements that are to be added into one list "toBeAdded"
        toBeAdded = []
        prev = 0
        for index in addIndices:
            toBeAdded.append(string[prev:index])
            prev = index + 1
            if index == addIndices[-1]:
                toBeAdded.append(string[index + 1 :])
            
        # we then create a string ready to be evaluated by lillepy by iterating
        # through the toBeAdded elements.
        addString = "lp.Add("
        for obj in toBeAdded:
            if ("(" in obj) and ("+" in obj):
                # if there is a parenthesis in the object that is to be added,
                # it needs to be parsed again
                leftParIndex = obj.index("(")
                rightParIndex = Parser.locateClosingParenthesis(obj, leftParIndex)
                obj = (
                    obj[:leftParIndex]
                    + "("
                    + Parser.parseAdd(
                        obj[leftParIndex + 1 : rightParIndex + 1], isChild=True
                    )
                    + ")"
                )
            addString += obj + ","

        # if the parseAdd method has been called recursively, i.e isChild = True, then
        # we will NOT add the final closing parenthesis
        if not isChild:
            return addString[:-1] + ")"
        else:
            return addString[:-1]

    def parseMul(string, isChild=False):
        ''' In a normal parsing sequence, the parseMul method would be called
            right after parseMul'''


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


foo = "(2+3)*456"
res = Parser.parseAdd(foo)
print(res)
