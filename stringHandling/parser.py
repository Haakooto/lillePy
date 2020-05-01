
class Parser:
    def parseAdd(string, isChild = False):
        # isChild is documented below
        '''this method will replace the elemtens added in a string with a
        lillepy-expression on the form: a+b+c -> lp.Add(a,b,c)'''

        #remove any whitespace from the string
        string = string.replace(' ','')

        build = '' # empty string to be constructed into the parsed result

        addIndices = Parser.locateSymbol(string, "+")
        iterString = iter(enumerate(string)) # iteratable object
        for index, obj in iterString:

            if obj == '+':
                build += ','

            elif obj == "(":
                #locate the opening and closing pars
                opening = index
                closing = Parser.locateClosingParenthesis(string, index)

                '''if there are no additions in the parenthesis, we of course skip this section.
                However we need to be careful when checking the section for plus signs,
                as any plussigns within another parenthesises will NOT count towards
                deciding wether our surrent parenthesis group has addidion in it'''
                parSections = Parser.locateParSections(string[opening+1:closing])
                searchString = Parser.cutSections(string[opening+1:closing][:], parSections)
                if '+' not in searchString:
                    build += '('
                    continue

                '''next we determine if the par is either a function call or a group.
                    we do this because in some instances,
                    we wish to keep the parenthesis, i.e in sin(2+x)->sin(lp.Add(2,x)),
                    and in some cases, we do no not, i.e (2+3)*8 -> lp.Add(2,3)*8'''
                isFuncGroup = Parser.parIsFunctionGroup(string, index)
                if isFuncGroup:
                    optionalPar = {'L':'(', 'R':')'}
                else:
                    optionalPar = {'L':'', 'R':''}

                # we add to the build
                build += f'{optionalPar["L"]}lp.Add({Parser.parseAdd(string[opening+1:closing], isChild=True)}){optionalPar["R"]}'

                #Finally we continue past the parenthesis with the next() function
                for foo in range(closing-opening):
                    next(iterString)

            else:
                build += obj
        '''We will only add an lp.Add() around the return object if the called parse
            is not a child of any other ongoing parse.'''
        if isChild:
            return build
        else:
            return f'lp.Add({build})'


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

    def parIsFunctionGroup(string, index):
        '''THIS NEEDS TO BE OPTIMIZED'''
        '''OPTIMIZE WITH REGEX'''

        ''' index must be the index of the opening parenthesis in a string.
        will return False in cases like 4*(2+3) and 4-(2+x) and
        True in cases like sin(7+2) and log(3+x)
        '''

        # We iterate "backwards" through the string, in order to catch the
        # first instance of a matching function name.
        stringBwd = string[:index][::-1]
        fNamesBwd = sorted([foo[::-1] for foo in fNames], key=len, reverse=True) #fNames with the names backwards sorted by length, decreasing
        for fName in fNamesBwd:
            if stringBwd[:len(fName)] == fName:
                return True
        return False

    def locateParSections(string):
        '''This method locates all the closed parenthesis sections withing the string
            and returns them all in a nested list'''
        res = []
        for i,obj in enumerate(string):
            if obj =='(':
                res.append([i, Parser.locateClosingParenthesis(string,i)])
        return res

    def cutSections(string, sections):
        '''section is a nested list of lists of length 2 with the indexes of sections to be removed from the string'''
        letterList = list(string)
        for sec in sections:
            del letterList[sec[0]:sec[1]]
        return str(letterList)


fNames = ['sin', 'cos', 'tan','log','ln', 'arcsin','arccos', 'acos','asin']


foo = "2+sin(34*(2+1))*(2+3)"
res = Parser.parseAdd(foo)
print(res)
