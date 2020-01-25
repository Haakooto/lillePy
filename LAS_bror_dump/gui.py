from tkinter import *
from custom_functions import *
from main_functions import *
from interpreter_bror import *
import write_manager as wm
root = Tk()
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='LAS.png'))
def get_e1():

    selections = ['Math mode', 'Define Function', 'Delete Function']
    mode_selection = selections[listbox.curselection()[0]]

    x = Variable('x')
    input = e1.get()



    #this makes sure that all custom functiosn get defined
    for func in  wm.get_func_list():
        exec(func + '=getfunc("'+func+'")')


    if mode_selection == 'Math mode':
        try:
            text.insert(END,input+'='+str(eval(input))+'\n')
        except NameError:
            text.insert('end', 'No function "tan(x)" defined', 'fail')

    if mode_selection == 'Define Function':

        func_name = input[:input.find('=')]
        func_def = input[input.find('=')+1:]
        if func_name[-3:] == '(x)':
            func_name = func_name[:-3]


        func = customFunction(func_def)
        was_written = func.set_name(func_name)
        if was_written:
            text.insert('end', 'Defined '+ input + '.\n', 'success')
        elif not was_written:
            text.insert('end', 'Function "'+func_name+'" not defined. Name already taken.\n', 'fail')




    if mode_selection == 'Delete Function':
        func_name = input
        if func_name[-3:] == '(x)':
            func_name = func_name[:-3]
        was_deleted = delfunc(func_name)
        print(was_deleted)
        if was_deleted:
            text.insert('end','Deleted function "'+func_name+'".\n', 'success')
        elif not was_deleted:
            text.insert('end', 'No stored function with name "'+func_name+'".\n', 'fail')

    #text.insert(END, '\n'+e1.get())

#main entrty widget
e1 = Entry(root, width = 20)
e1.grid(row=1, column = 0)


button = Button(root, text='Go', command=get_e1).grid(row=1, column = 1)
text = Text(root, width=60,)
text.grid(row=0)

listbox = Listbox(root, width=15)
listbox.insert(1,'Math mode')
listbox.insert(2,'Define Function')
listbox.insert(3, 'Delete Function')

listbox.grid(row=0, column=1)
listbox.activate(index=0)

#tags for colorschemes
text.tag_config('success', background="snow2", foreground="green4")
text.tag_config('fail', background="snow2", foreground="red3")


root.mainloop()
root.destroy()
