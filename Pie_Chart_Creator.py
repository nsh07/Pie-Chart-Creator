import os
import sys
import string
import webbrowser
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
import pygame
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class _Entry:
    '''
    An Entry widget that have temporary text(like a placeholder in HTML).
    It also lets user to remove text upto the nearest left delimiter
    '''

    def __init__(self, frame, DefaultText):
        self.IsDefault = True
        self.EntriesFrame = frame
        self.DefaultText = DefaultText
        self.StyleName = f'{DefaultText}.TEntry'

        self.var = StringVar()
        self.Style = ttk.Style()
        self.Style.configure(self.StyleName, foreground='grey')

        self.Entry = ttk.Entry(self.EntriesFrame, justify=CENTER, width=35, style=self.StyleName, textvariable=self.var)
        self.SetDefault()

        self.Entry.bind('<FocusIn>', self.FocusIn)
        self.Entry.bind('<FocusOut>', self.FocusOut)
        self.Entry.bind('<Control-BackSpace>', self.ControlBackSpace)

    def FocusIn(self, event=None):
        '''
        When user clicks to respective entry widget
        '''

        if self.IsDefault:
            self.IsDefault = False
            self.var.set('')
            self.Style.configure(self.StyleName, foreground='black')

    def FocusOut(self, event=None):
        '''
        When user clicks out of respective entry widget
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.SetDefault()

    def SetDefault(self):
        '''
        Set the default state of respective entry widget
        '''

        self.IsDefault = True
        self.var.set(self.DefaultText)
        self.Style.configure(self.StyleName, foreground='grey')

    def ControlBackSpace(self, event=None):
        '''
        Delete characters upto the nearest delimiter
        from the current position of the cursor
        '''

        StartIndex = None
        VarGet = self.var.get().strip()
        EndIndex = self.Entry.index('insert')

        if self.DefaultText == 'Items':
            delimiter = string.punctuation + ' '

        else:
            delimiter = '.'

        if VarGet:
            # Getting index of the nearest delimiter
            # before the position of the cursor
            for idx in range(EndIndex - 1, -1, -1):
                if VarGet[idx] in delimiter:
                    StartIndex = idx
                    break

            if StartIndex and StartIndex + 1 == EndIndex:
                StartIndex = EndIndex - 2

            elif StartIndex is None:
                StartIndex = -1

            self.Entry.delete(StartIndex + 1, EndIndex)

            return 'break'


class PieCharCreator:
    def __init__(self, win):
        pygame.mixer.init()

        if sys.platform == 'win32':
            pygame.mixer.music.load(self.ResourcePath('WinErrSound.wav'))

        else:
            pygame.mixer.music.load(self.ResourcePath('LinuxErrSound.wav'))

        matplotlib.use('TkAgg')
        self.IsItFirstTime = True
        self.Details = {'Python': (100.0, 0.1)}

        self.master = win
        self.master.withdraw()
        self.master.config(bg='white')
        self.master.title('Pie Chart Creator')

        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.master.iconphoto(False, self.IconImage)

        self.TitleImage = PhotoImage(file=self.ResourcePath('PCC_Logo.png'))

        self.TopFrame = Frame(self.master)
        self.TopFrame.pack()

        self.LeftFrame = Frame(self.TopFrame, bg='white')
        self.LeftFrame.pack(side=LEFT, fill='y')

        self.TitleLabel = Label(self.LeftFrame, image=self.TitleImage, bd=0, cursor='hand2')
        self.TitleLabel.pack()

        self.EntriesFrame = Frame(self.LeftFrame, bg='white')
        self.EntriesFrame.pack(pady=3)

        self.ItemEntry = _Entry(self.EntriesFrame, 'Items')
        self.ItemEntry.Entry.pack(ipady=3, pady=3)
        self.ValueEntry = _Entry(self.EntriesFrame, 'Values')
        self.ValueEntry.Entry.pack(ipady=3, pady=3)

        # Adding Radio Buttons widgets
        self.RadioButtonVar = IntVar()
        self.RadioButtonVar.set(-1)
        self.RadioButtonStyle = ttk.Style()
        self.RadioButtonStyle.configure('R.TRadiobutton', background='white')

        self.ExplodeFrame = LabelFrame(self.LeftFrame, text='Explode', bg='white')
        self.ExplodeFrame.pack(ipady=2, pady=3)

        self.EnableRadio = ttk.Radiobutton(self.ExplodeFrame, text='Enable', variable=self.RadioButtonVar, value=1, cursor='hand2', style='R.TRadiobutton')
        self.EnableRadio.pack(side=LEFT, ipadx=45, ipady=5)

        self.DisableRadio = ttk.Radiobutton(self.ExplodeFrame, text='Disable', variable=self.RadioButtonVar, value=2, cursor='hand2', style='R.TRadiobutton')
        self.DisableRadio.pack(side=LEFT)

        # Adding Buttons widgets
        self.ButtonsFrame = Frame(self.LeftFrame, bg='white')
        self.ButtonsFrame.pack()

        self.AddButton = Button(self.ButtonsFrame, text='ADD', width=30, bd=0, bg='green', activebackground='green', fg='white', activeforeground='white', cursor='hand2', relief=GROOVE, command=self.AddCommand)
        self.AddButton.pack(ipady=7, pady=3)

        # Adding TreeView widget
        self.TreeFrame = Frame(self.TopFrame, bg='white')
        self.TreeFrame.pack(side=RIGHT, fill='both')

        self.Columns = ['ITEMS', 'VALUES', 'EXPLODE']

        self.TreeStyle = ttk.Style()
        self.TreeStyle.configure('MyStyle.Treeview')
        self.Tree = ttk.Treeview(self.TreeFrame, columns=self.Columns, show='headings', height=12, style='MyStyle.Treeview')
        self.Tree.pack(side=LEFT)

        self.Tree.heading('ITEMS', text='ITEMS')
        self.Tree.column('ITEMS', width=250, anchor='center')
        self.Tree.heading('VALUES', text='VALUES')
        self.Tree.column('VALUES', width=100, anchor='center')
        self.Tree.heading('EXPLODE', text='EXPLODE')
        self.Tree.column('EXPLODE', width=80, anchor='center')

        self.Tree.tag_configure('odd', background='#DFDFDE', foreground='#687980')
        self.Tree.tag_configure('even', background='#EEEEEE', foreground='#687980')

        # Attaching scrollbar to TreeView
        self.scrollbar = Scrollbar(self.TreeFrame, orient="vertical", command=self.Tree.yview)
        self.Tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill='y')

        # Adding plot
        self.BottomFrame = Frame(self.master, bg='white')
        self.BottomFrame.pack(fill='both')

        self.fig = Figure() # create a figure object
        self.ax = self.fig.add_subplot(111) # add an Axes to the figure

        self.PlotCanvas = FigureCanvasTkAgg(self.fig, master=self.BottomFrame)
        self.PlotWidget = self.PlotCanvas.get_tk_widget()
        self.PlotWidget.config(height=300)
        self.PlotWidget.pack(side=LEFT)

        self.ToolBar = VerticalNavigationToolbar2Tk(self.PlotCanvas, self.BottomFrame)
        self.ToolBar.config(background='white')
        self.ToolBar.update()
        self.ToolBar.place(x=580, y=35)

        for button in self.ToolBar.winfo_children():
            if isinstance(button, Label):
                button.config(background='white')

        self.DrawPieChart()
        self.InitialPosition()

        self.Tree.bind('<Button-3>', self.RightClick)
        self.master.bind('<Button-1>', self.FocusAnyWhere)
        self.master.bind('<Delete>', self.RemoveSelection)
        self.TitleLabel.bind('<Button-1>', self.OpenGithub)
        self.ItemEntry.Entry.bind('<Return>', self.AddCommand)
        self.ValueEntry.Entry.bind('<Return>', self.AddCommand)
        self.Tree.bind('<Motion>', self.RestrictDefaultBindings)
        self.master.protocol('WM_DELETE_WINDOW', self.master.quit)
        self.Tree.bind('<Button-1>', self.RestrictDefaultBindings)

    def InitialPosition(self):
        '''
        Set window position to the center when program starts first time
        '''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width()
        ScreenWidth = self.master.winfo_screenwidth() // 2

        self.master.geometry(f'+{ScreenWidth - width // 2}+15')
        self.master.deiconify()

    def RestrictDefaultBindings(self, event):
        '''
        Restrict user to resize the columns of Treeview
        '''

        if self.Tree.identify_region(event.x, event.y) == "separator":
            return "break"

        elif self.ClickedAtEmptySpace(event) and event.num == 1:
            self.Tree.selection_remove(*self.Tree.selection())
            self.Tree.focus_set()

            return 'break'

    def FocusAnyWhere(self, event):
        '''
        Change focus to clicked widget
        '''

        event.widget.focus()

    def AddCommand(self, event=None):
        '''
        When user clicks add button
        '''

        label = self.ItemEntry.var.get()
        value = self.ValueEntry.var.get()
        is_digit = value.lstrip('-').replace('.', '', 1).replace('e-', '', 1).replace('e', '', 1).isdigit()

        error_label = Label(self.master, fg='red', bg='white', font=Font(size=15, weight='bold'))

        if self.ItemEntry.IsDefault:
            pygame.mixer.music.play()
            error_label.config(text='Invalid item')
            error_label.place(x=85, y=280)

            self.master.after(1500, error_label.place_forget)

        elif self.ValueEntry.IsDefault or is_digit is False:
            pygame.mixer.music.play()
            error_label.config(text='Invalid value')
            error_label.place(x=85, y=280)

            self.master.after(1500, error_label.place_forget)

        else:
            explode = self.RadioButtonVar.get()

            if explode == -1:
                explode = 2

            # When the first value is added for the first
            # time then removing the default value and then
            # adding user entered value
            if self.IsItFirstTime:
                self.Details.clear()
                self.IsItFirstTime = False

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

            self.RadioButtonVar.set(-1)

            self.ItemEntry.SetDefault()
            self.ValueEntry.SetDefault()

            self.ItemEntry.Entry.focus()

            self.DrawPieChart()

    def DrawPieChart(self):
        '''
        Draw Pie Chart from the values entered by user
        '''

        self.ax.clear()

        labels = list(self.Details.keys())
        values = list(map(lambda i: i[0], self.Details.values()))
        explodes = list(map(lambda i: 0.15 if i[1] == 1 else 0, self.Details.values()))

        self.ax.pie(values, explode=explodes, labels=labels, autopct='%0.2f%%', shadow=True)
        self.PlotCanvas.draw_idle()

    def ClickedAtEmptySpace(self, event=None):
        '''
        Check if user has clicked in empty space
        '''

        return self.Tree.identify('item', event.x, event.y) == ''

    def RightClick(self, event=None):
        '''
        When user right clicks inside list-box
        '''

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
        '''
        Clear all values from treeview and pie-chart at once
        '''

        self.IsItFirstTime = True
        self.Details = {'Python': (100.0, 0.1)}
        self.Tree.delete(*self.Tree.get_children())

        self.DrawPieChart()

    def RemoveSelection(self, event=None):
        '''
        Remove the selected value from the treeview and pie-chart
        '''

        selections = self.Tree.selection()

        for selection in selections:
            values = self.Tree.item(selection)['values']
            self.Details.pop(values[0])

        self.Tree.delete(*selections)

        if not self.Details:
            self.IsItFirstTime = True
            self.Details = {'Python': (100.0, 0.1)}

        self.DrawPieChart()

    def OpenGithub(self, event=None):
        '''
        Open Github page of project when user clicks title image
        '''

        webbrowser.open('https://github.com/NMrocks/Pie-Chart-Creator')

    def ResourcePath(self, FileName):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

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
