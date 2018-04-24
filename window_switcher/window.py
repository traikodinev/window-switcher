from tkinter import Entry, Listbox, StringVar
import sys, tkinter, subprocess
from window_switcher.aux import get_windows

class Window:
    FONT = ('Monospace', 11)
    ITEM_HEIGHT = 22
    MAX_FOUND = 10
    BG_COLOR = '#202b3a'
    FG_COLOR = '#ced0db'

    def resize(self, items):
        if self.resized:
            return
        
        self.root.geometry(f'{self.width}x{self.height + items * Window.ITEM_HEIGHT}')
        self.resized = True

    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.all_windows = []
        self.resized = False

        # master.geometry(500)
        root.title("window switcher")
        root.resizable(width=False, height=False)
        root.configure(background=Window.BG_COLOR)
        
        # ugly tkinter code below
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.on_entry(sv))

        self.main_entry = Entry(
            root,
            font=Window.FONT,
            width=1000,
            textvariable=sv,
            bg=Window.BG_COLOR,
            fg=Window.FG_COLOR,
            insertbackground=Window.FG_COLOR,
            bd=0
        )
        self.main_entry.grid(row=0, column=0, padx=10)
        self.main_entry.focus_set()

        self.listbox = Listbox(
            root,
            height=Window.ITEM_HEIGHT,
            font=Window.FONT,
            highlightthickness=0,
            borderwidth=0,
            bg=Window.BG_COLOR,
            fg=Window.FG_COLOR,
            selectbackground='#2c3c51',
            selectforeground='#cedaed'
        )
        self.listbox.grid(row=1, column=0, sticky='we', padx=10, pady=10)

        # key bindings
        self.main_entry.bind('<Control-a>', self.select_all)
        self.main_entry.bind('<Up>', self.select_prev)
        self.main_entry.bind('<Down>', self.select_next)
        self.main_entry.bind('<Return>', self.select_window)
        self.root.bind('<Escape>', lambda e: sys.exit())

        # self.resize(Window.MAX_FOUND)
        self.initial_get(None)

    def initial_get(self, event):
        self.all_windows = get_windows()
        self.find_windows('')

    def select_all(self, event):
        # select text
        self.main_entry.select_clear()
        self.main_entry.select_range(0, 'end')
        # move cursor to the end
        self.main_entry.icursor('end')

        return 'break'

    def find_windows(self, text):
        text = text.lower()

        found = [window for window in self.all_windows if window['name'].find(text) != -1]
        # print(found)

        self.found = found

        self.listbox.delete(0, 'end')

        for i, item in enumerate(found):
            if i >= Window.MAX_FOUND:
                break
            self.listbox.insert('end', item['name'])

        self.resize(min(len(found), Window.MAX_FOUND))

        # select first element
        self.listbox.selection_set(0)

    def select_next(self, event):
        if len(self.found) == 0:
            return 

        idx = self.listbox.curselection()[0]
        max = self.listbox.size()
        idx += 1
        if idx >= max:
            idx = 0

        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(idx)

    def select_prev(self, event):
        if len(self.found) == 0:
            return

        idx = self.listbox.curselection()[0]
        max = self.listbox.size()
        idx -= 1
        if idx < 0:
            idx = max - 1

        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(idx)

    def select_window(self, event):
        idx = self.listbox.curselection()[0]
        id = self.found[idx]['id']

        # switch to window and exit
        # wmctrl -ia <id`>
        subprocess.call(['wmctrl', '-ia', id])
        # print(subprocess.check_output(['wmctrl', '-ia', id]).decode('utf-8'))

        sys.exit(0)


    def on_entry(self, newtext):
        search_test = newtext.get()
        self.find_windows(search_test)
        return True
