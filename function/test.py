import sys
import linecache
import os
def traceit(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        res =  linecache.getline('test.py', lineno)
        print(lineno)
    return traceit

class test:
    def __init__(self,a):
        print('a')

sys.settrace(os.execv(__file__, sys.argv))

cool = test(1)
