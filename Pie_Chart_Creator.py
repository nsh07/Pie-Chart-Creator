import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
import pygame
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class PieCharCreator:
    def __init__(self, win):
        pygame.mixer.init()

        if sys.platform == 'win32':
            pygame.mixer.music.load(self.ResourcePath('WinErrSound.wav'))

        else:
            pygame.mixer.music.load(self.ResourcePath('LinuxErrSound.wav'))

        matplotlib.use('TkAgg')
        self.is_it_first_time = True
        self.Details = {'Python': (100.0, 0.1)}

        self.is_item_default_value_cleared = False
        self.is_value_default_value_cleared = False

        self.master = win
        self.master.withdraw()
        self.master.config(bg='white')
        self.master.title('Pie Chart Creator')

        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.master.iconphoto(False, self.IconImage)

        self.TitleImage = PhotoImage(file=self.ResourcePath('PCC_Logo.png'))

        self.top_frame = Frame(self.master)
        self.top_frame.pack()

        self.left_frame = Frame(self.top_frame, bg='white')
        self.left_frame.pack(side=LEFT, fill='y')

        self.title_label = Label(self.left_frame, image=self.TitleImage, bd=0)
        self.title_label.pack()

        self.entries_frame = Frame(self.left_frame, bg='white')
        self.entries_frame.pack(pady=3)

        # Adding Entries widgets
        self.items_style = ttk.Style()
        self.value_style = ttk.Style()
        self.items_style.configure('I.TEntry', foreground='grey')
        self.value_style.configure('V.TEntry', foreground='grey')
        self.styles_list = {self.items_style: 'I.TEntry', self.value_style: 'V.TEntry'}

        self.item_entry_var = StringVar()
        self.item_entry = ttk.Entry(self.entries_frame, justify=CENTER, width=35, style='I.TEntry', textvariable=self.item_entry_var)
        self.item_entry.pack(ipady=3, pady=3)

        self.value_entry_var = StringVar()
        self.value_entry = ttk.Entry(self.entries_frame, justify=CENTER, width=35, style='V.TEntry', textvariable=self.value_entry_var)
        self.value_entry.pack(ipady=3, pady=3)

        for widget, text in {self.item_entry: 'Items', self.value_entry: 'Values'}.items():
            widget.insert(END, text)

        # Adding Radio Buttons widgets
        self.radio_button_var = IntVar()
        self.radio_button_var.set(-1)
        self.radio_button_style = ttk.Style()
        self.radio_button_style.configure('R.TRadiobutton', background='white')

        self.explode_frame = LabelFrame(self.left_frame, text='Explode', bg='white')
        self.explode_frame.pack(ipady=2, pady=3)

        self.enable_radio = ttk.Radiobutton(self.explode_frame, text='Enable', variable=self.radio_button_var, value=1, cursor='hand2', style='R.TRadiobutton')
        self.enable_radio.pack(side=LEFT, ipadx=45, ipady=5)

        self.disable_radio = ttk.Radiobutton(self.explode_frame, text='Disable', variable=self.radio_button_var, value=2, cursor='hand2', style='R.TRadiobutton')
        self.disable_radio.pack(side=LEFT)

        # Adding Buttons widgets
        self.buttons_frame = Frame(self.left_frame, bg='white')
        self.buttons_frame.pack()

        self.add_button = Button(self.buttons_frame, text='ADD', width=30, bd=0, bg='green', activebackground='green', fg='white', activeforeground='white', cursor='hand2', relief=GROOVE, command=self.AddCommand)
        self.add_button.pack(ipady=7, pady=3)

        # Adding TreeView widget
        self.tree_frame = Frame(self.top_frame, bg='white')
        self.tree_frame.pack(side=RIGHT, fill='both')

        self.Columns = ['ITEMS', 'VALUES', 'EXPLODE']

        self.tree_style = ttk.Style()
        self.tree_style.configure('MyStyle.Treeview')
        self.Tree = ttk.Treeview(self.tree_frame, columns=self.Columns, show='headings', height=12, style='MyStyle.Treeview')
        self.Tree.pack(side=LEFT)

        self.Tree.heading('ITEMS', text='ITEMS')
        self.Tree.column('ITEMS', width=250, anchor='center')
        self.Tree.heading('VALUES', text='VALUES')
        self.Tree.column('VALUES', width=100, anchor='center')
        self.Tree.heading('EXPLODE', text='EXPLODE')
        self.Tree.column('EXPLODE', width=80, anchor='center')

        # Attaching scrollbar to TreeView
        self.scrollbar = Scrollbar(self.tree_frame, orient="vertical", command=self.Tree.yview)
        self.Tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill='y')

        # Adding plot
        self.bottom_frame = Frame(self.master, bg='white')
        self.bottom_frame.pack(fill='both')

        self.fig = Figure() # create a figure object
        self.ax = self.fig.add_subplot(111) # add an Axes to the figure

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
        self.plot_widget = self.plot_canvas.get_tk_widget()
        self.plot_widget.config(height=300)
        self.plot_widget.pack(side=LEFT)

        self.toolbar = VerticalNavigationToolbar2Tk(self.plot_canvas, self.bottom_frame)
        self.toolbar.config(background='white')
        self.toolbar.update()
        self.toolbar.place(x=580, y=35)

        for button in self.toolbar.winfo_children():
            if isinstance(button, Label):
                button.config(background='white')

        self.pie_entries = (self.item_entry, self.value_entry, self.radio_button_var)

        self.DrawPieChart()
        self.InitialPosition()

        self.Tree.bind('<Button-3>', self.RightClick)
        self.item_entry.bind('<Return>', self.AddCommand)
        self.value_entry.bind('<Return>', self.AddCommand)
        self.master.bind('<Button-1>', self.master_bindings)
        self.item_entry.bind('<FocusIn>', self.entry_bindings)
        self.value_entry.bind('<FocusIn>', self.entry_bindings)
        self.Tree.bind('<Motion>', self.RestrictDefaultBindings)
        self.master.protocol('WM_DELETE_WINDOW', self.master.quit)
        self.Tree.bind('<Button-1>', self.RestrictDefaultBindings)
        self.enable_radio.bind('<FocusIn>', self.entry_bindings)

    def run(self):
        self.master.mainloop()

    def InitialPosition(self):
        '''Set window position to the center when program starts first time'''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width()
        screen_width = self.master.winfo_screenwidth() // 2

        self.master.geometry(f'+{screen_width - width // 2}+15')
        self.master.deiconify()

    def RestrictDefaultBindings(self, event):
        '''Restrict user to resize the columns of Treeview '''

        if self.Tree.identify_region(event.x, event.y) == "separator":
            return "break"

        elif self.ClickedAtEmptySpace(event) and event.num == 1:
            self.Tree.selection_remove(*self.Tree.selection())
            self.Tree.focus_set()
            self.entry_bindings(event)

            return 'break'

    def master_bindings(self, event=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        widget = event.widget
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'), self.value_entry: (self.value_style, 'V.TEntry')}

        for wid in entries_widgets:
            if not wid.get().strip() and widget != self.prev_widget:
                wid.delete(0, END)
                wid.insert(END, entries_widgets[wid])

                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

        if not isinstance(widget, ttk.Entry):
            self.master.focus()

        if widget != self.Tree:
            self.Tree.selection_remove(*self.Tree.selection())

    def entry_bindings(self, event=None):
        '''When user clicks in or out of the entries widget'''

        widget = event.widget
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'),
                          self.value_entry: (self.value_style, 'V.TEntry')}

        if widget in entries_widgets:
            if widget.get().strip() == entries_widgets[widget]:
                widget.delete(0, END)
                self.prev_widget = widget

                if widget == self.item_entry:
                    self.is_item_default_value_cleared = True

                else:
                    self.is_value_default_value_cleared = True

                style, style_name = entries_styles[widget]
                style.configure(style_name, foreground='black')

                entries_widgets.pop(widget)
                entries_styles.pop(widget)

        for wid in entries_widgets:
            if not wid.get().strip():
                wid.delete(0, END)
                wid.insert(END, entries_widgets[wid])

                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

                if widget == self.item_entry:
                    self.is_item_default_value_cleared = False

                else:
                    self.is_value_default_value_cleared = False

        widget.focus()

    def AddCommand(self, event=None):
        '''When user clicks add button'''

        label = self.item_entry_var.get()
        value = self.value_entry_var.get()
        is_digit = value.lstrip('-').replace('.', '', 1).replace('e-', '', 1).replace('e', '', 1).isdigit()

        error_label = Label(self.master, fg='red', bg='white', font=Font(size=15, weight='bold'))

        if self.is_item_default_value_cleared is False:
            pygame.mixer.music.play()
            error_label.config(text='Invalid item')
            error_label.place(x=85, y=280)

            self.master.after(1500, error_label.place_forget)

        elif self.is_value_default_value_cleared is False or is_digit is False:
            pygame.mixer.music.play()
            error_label.config(text='Invalid value')
            error_label.place(x=85, y=280)

            self.master.after(1500, error_label.place_forget)

        else:
            explode = self.radio_button_var.get()
            self.is_item_default_value_cleared = False
            self.is_value_default_value_cleared = False

            if explode == -1:
                explode = 2

            if self.is_it_first_time:
                self.Details.clear()
                self.is_it_first_time = False

            self.Details[label] = (value, explode)

            labels = list(self.Details.keys())
            values = list(map(lambda i: i[0], self.Details.values()))
            explodes = list(map(lambda i: 'Enabled' if i[1] == 1 else 'Disabled', self.Details.values()))

            self.Tree.delete(*self.Tree.get_children())

            for index in range(len(labels)):
                val = (labels[index], values[index], explodes[index])

                if index % 2 == 0:
                    tags = ('even', )

                else:
                    tags = ('odd', )

                self.Tree.insert('', END, values=val, tags=tags)

            self.Tree.tag_configure('odd', background='#DFDFDE', foreground='#687980')
            self.Tree.tag_configure('even', background='#EEEEEE', foreground='#687980')

            self.item_entry_var.set('Items')
            self.value_entry_var.set('Values')
            self.radio_button_var.set(-1)

            self.items_style.configure('I.TEntry', foreground='grey')
            self.value_style.configure('V.TEntry', foreground='grey')

            self.item_entry.focus()
            self.DrawPieChart()

    def DrawPieChart(self):
        '''Draw Pie Chart from the values entered by user'''

        self.ax.clear()

        labels = list(self.Details.keys())
        values = list(map(lambda i: i[0], self.Details.values()))
        explodes = list(map(lambda i: 0.15 if i[1] == 1 else 0, self.Details.values()))

        self.ax.pie(values, explode=explodes, labels=labels, autopct='%0.2f%%', shadow=True)
        self.plot_canvas.draw_idle()

    def ClickedAtEmptySpace(self, event=None):
        '''Check if user has clicked in empty space'''

        return self.Tree.identify('item', event.x, event.y) == ''

    def RightClick(self, event=None):
        '''When user right clicks inside list-box'''

        x, y = event.x , event.y  # Cursor position with respect to Tk window
        CurrentSelection = self.Tree.selection()
        RightClickMenu = Menu(self.master, tearoff=False)

        if CurrentSelection:
            RightClickMenu.add_command(label='Remove Selection(s)', command=self.RemoveSelection)
            RightClickMenu.add_command(label='Clear ALL', command=self.ClearAll)

        elif self.ClickedAtEmptySpace(event):
            if self.Tree.get_children():
                RightClickMenu.add_command(label='Clear ALL', command=self.ClearAll)

        else:
            self.Tree.event_generate('<Button-1>', x=x, y=y)
            self.RightClick(event)

        try:
            RightClickMenu.tk_popup(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def ClearAll(self, event=None):
        '''Clear all values from treeview and pie-chart at once'''

        self.is_it_first_time = True
        self.Details = {'Python': (100.0, 0.1)}
        self.Tree.delete(*self.Tree.get_children())

        self.DrawPieChart()

    def RemoveSelection(self, event=None):
        '''Remove the selected value from the treeview and pie-chart'''

        selections = self.Tree.selection()

        for selection in selections:
            values = self.Tree.item(selection)['values']
            self.Details.pop(values[0])

        self.Tree.delete(*selections)

        if not self.Details:
            self.is_it_first_time = True
            self.Details = {'Python': (100.0, 0.1)}

        self.DrawPieChart()

    def ResourcePath(self, FileName):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'included_files', FileName)


class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):
    def __init__(self, canvas, window):
        super().__init__(canvas, window, pack_toolbar=False)

    def _Button(self, text, image_file, toggle, command):
        # override _Button() to re-pack the toolbar button in vertical direction
        b = super()._Button(text, image_file, toggle, command)
        b.pack(side=TOP) # re-pack button in vertical direction

        return b

    def _Spacer(self):
        # override _Spacer() to create vertical separator
        s = Frame(self, width=26, relief=RIDGE, bg="DarkGray", padx=2)
        s.pack(side=TOP, pady=5) # pack in vertical direction

        return s

    def set_message(self, s):
        # disable showing mouse position in toolbar
        pass


if __name__ == "__main__":
    win = Tk()
    chart = PieCharCreator(win)
    win.mainloop()
