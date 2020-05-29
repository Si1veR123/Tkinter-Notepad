from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os

text_contents = {}

def create_file(content='', title='Untitled'):
    container = ttk.Frame(notebook) # frame for the text area. allows scroll bar
    container.pack()

    text_area = Text(container)
    text_area.insert("end", content) # insert any given content at end of text
    text_area.pack(side='left', fill='both', expand=True)

    notebook.add(container, text=title)
    notebook.select(container) # select the new window
    text_contents[str(text_area)] = hash(content) # updates the dictionary with the 'text_area:hash(of content)'
    # str(text_area) is a string representing the text area. Unique to each area

    text_scroll = ttk.Scrollbar(text_area, orient='vertical', command=text_area.yview) # make scrollbar to scroll text_area
    text_scroll.pack(side='right', fill='y')

    text_area['yscrollcommand'] = text_scroll.set


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path) # get the filename from path e.g. user/documents/txt returns 'txt'
        tab_widget = root.nametowidget(notebook.select())
        text_widget = tab_widget.winfo_children()[0] # the tab widget contains the text and the scrollbar. get widget info (winfo) returns children
        # select - returns widget name of currently selected pane, if no arg is given
        # nametowidget returns the instance of the tkinter widget by given name
        # all this line does is get the tkinter instance of the selected text window

        content = text_widget.get('1.0', 'end-1c')
        # this gets the content of the textwindow, from 1st char of 0th line, to end.
        # tkinter creates line at end, '-1c' removes the final 'new line character'

        with open(file_path, 'w') as file:
            file.write(content)

    except (AttributeError, FileNotFoundError) as e:
        print(e, 'Error. Cancelled Save.')
        return

    notebook.tab('current', text=filename) # renames current notebook tab to the saved filename
    text_contents[str(text_widget)] = hash(content) # updates changes when saved

def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path)

        with open(file_path, 'r') as file:
            content = file.read()

    except (AttributeError, FileNotFoundError) as e:
        print(e, 'Error. Cancelled Open.')
        return

    create_file(content, filename)

def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = root.nametowidget(notebook.select())
        text_widget = tab_widget.winfo_children()[0]
        content = text_widget.get('1.0', 'end-1c')

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved:
        confirm = messagebox.askyesno(
            message='Unsaved changes. Are you sure you want to quit?',
            icon='question',
            title='Confirm Quit'
        )
        if not confirm:
            return
    root.destroy()

def check_changes():
    tab_widget = root.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0]
    try:
        content = text_widget.get('1.0', 'end-1c')
    except AttributeError:
        return
    saved_content = text_contents[str(text_widget)]
    name = notebook.tab('current')['text']

    if hash(content) != saved_content: # if changes have been made
        if name[-1] != '*': # and '*' isn't already on the filename
            notebook.tab('current', text=name+'*') # add it to the filename
    elif name[-1] == '*':
        notebook.tab('current', text=name[:-1])

def close_tab():
    tab_widget = root.nametowidget(notebook.select())
    current = tab_widget.winfo_children()[0]
    notebook.forget(current) # close current tab

root = Tk()
root.title('Tkinter Notepad')
root.geometry('600x800')
root.option_add('*tearOff', False) # prevents menu being torn off in some OS

main = ttk.Frame(root)
main.pack(fill='both', expand=True, padx=10, pady=(10, 0))
# the pady=(10, 0) means 10 pixels at top, none at bottom. padx has 10 padding on both sides


menubar = Menu()
root.config(menu=menubar)

file_menu = Menu(menubar) # a menu with parent of menubar
menubar.add_cascade(menu=file_menu, label='File') # makes a drop down menu

file_menu.add_command(label='New', command=create_file, accelerator='Ctrl+N') # UNSURE: this doesn't do anything but show shortcut next to the option. keybinds made below
file_menu.add_command(label='Open', command=open_file, accelerator='Ctrl+O')
file_menu.add_command(label='Save', command=save_file, accelerator='Ctrl+S')
file_menu.add_command(label='Close Current', command=close_tab, accelerator='Ctrl+Q')
file_menu.add_command(label='Exit', command=confirm_quit)

root.bind('<KeyPress>', lambda event:check_changes())
root.bind('<Control-n>', lambda event:create_file())
root.bind('<Control-s>', lambda event:save_file())
root.bind('<Control-o>', lambda event:open_file())
root.bind('<Control-q>', lambda event:close_tab())
# binds the keybind to the main window. this means shortcuts can be accessed without the menu being selected.
# .bind() second arg must be a function that takes an argument, even if we don't use it

notebook = ttk.Notebook(main)
notebook.pack(fill='both', expand=True)

create_file()

root.mainloop()