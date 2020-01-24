#a = (open('custom_functions_dir.txt', 'r').read().find('assert'))
#print(a)
#print(open('custom_functions_dir.txt', 'r').read()[a])
debug = True
import sys

def word_locator_string(word, string):
    pass

def symb_locator(line, symb, filename= "custom_functions_dir.txt"):
    file = open(filename, 'r')
    for i in range(line):
        file.readline()
    for char_index, char in enumerate(file.readline()):
        if char == symb:
            return char_index
    file.close()

def word_locator(word, filename= "custom_functions_dir.txt"):
    word_length = len(word)
    search_word = '|'+word+'|'

    word_start = open(filename, 'r').read().find(search_word)
    if word_start == -1:
        return None
    else:
        word_index = word_start+1,word_start+word_length+1
        return word_index

def line_locator(word, filename= "custom_functions_dir.txt"):
    lines = open(filename, 'r').readlines()
    search_word = '|'+word+'|'

    for i,line in enumerate(lines):
        if search_word in line:
            return i



def write_function(expr,fname):
    filename= "custom_functions_dir.txt"
    if word_locator(fname) is None:
        loc = word_locator(fname)
        line = line_locator(fname)
        write = open(filename, 'a')
        write.write(expr + '\n')
        write.close()
        if debug:
            print("wrote function " + fname)
    else:
        if debug:
            print('name "%s" already taken. No function stored' %fname)

def rewrite_function_name(old, new):
    filename= "custom_functions_dir.txt"
    line_no = line_locator(old)

    if line_no != -1:
        line = open(filename, 'r').readlines()[line_no]
        pos = line.find(old)
        line = line[:pos] + new + '|\n'
        data = open(filename, 'r').readlines()
        data[line_no] = line
        with open(filename, 'w') as file:
            file.writelines(data)
        if debug:
            print('renamed function %s to %s' %(old, new))
    else:
        if debug:
            print('attempted rewrite function name but no name "%s" found' %old)


def get_func(fname):
    filename= "custom_functions_dir.txt"
    line_no = line_locator(str(fname))
    if line_no is not None:
        line = open(filename, 'r').readlines()[line_no]
        pos = line.find('|'+ str(fname) +'|')
        func = line[:pos]
        return func

    else:
        if debug:
            print('ERROR: failed trying to retrieve function "%s"' %str(fname))
            sys.exit(1)


if __name__ == '__main__':
    print(get_func('tan'))
