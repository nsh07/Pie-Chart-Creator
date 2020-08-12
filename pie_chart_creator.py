import os
import sys
import webbrowser

try:  # Python 3
    import tkinter.tix as tix
    from tkinter import messagebox

except (ModuleNotFoundError, ImportError):  # Python 2
    import Tix as tix
    import tkMessageBox as messagebox

import requests
import matplotlib.pyplot as plt


def is_internet():
    '''Check if you are connected to internet'''

    try:
        requests.get('http://google.com')
        return True

    except requests.ConnectionError:
        return False


def center_window(_window, title):
    '''Set position of TopLevel or Tk window to the center of the screen'''

    _window.withdraw()

    _window.update()
    _window.title(title)
    _window.resizable(0, 0)
    _window.iconbitmap(resource_path('included_files\\icon.ico'))

    width, height = _window.winfo_width(), _window.winfo_height()
    _window.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

    _window.deiconify()


def open_link(event=None, _window=None):
    '''Open the github page of the author(NMrocks) in the default browser'''

    if is_internet():
        window.after(0, lambda: webbrowser.open('http://github.com/NMrocks/Pie-Chart-Creator'))

    else:
        messagebox.showerror('ERROR', 'Unable to load page because you are not connected to internet', parent=_window)


def append():
    '''Store data given by the user'''

    item = item_entry.get().title()
    percentage = percentage_entry.get()
    explode_ = explode_entry.get().title()

    if not item:
        messagebox.showerror('Invalid Input', 'Invalid name of item')

    elif percentage.isdigit():
        percentage = round(float(percentage), 2)

        pie_items.append(item)
        pie_items_percentage.append(percentage)

        if explode_ in ['Y', 'Yes']:
            explode.append(0.1)

        else:
            explode.append(0)

        for widget in [item_entry, percentage_entry, explode_entry]:
            widget.delete(0, tix.END)

    else:
        messagebox.showerror('Invalid Percentage', 'Percentage must be in number')


def show_register():
    '''Show stored data'''

    copy_pie_items = pie_items
    copy_pie_items_percentage = pie_items_percentage
    copy_explode = explode

    a = 0

    window.withdraw()
    register_window = tix.Toplevel()

    if pie_items:
        added_lbl_1 = tix.Label(register_window, text="Name of item", justify=tix.LEFT)
        added_lbl_1.grid(row=0, column=0, pady=5)

        added_lbl_2 = tix.Label(register_window, text="Percentage", justify=tix.LEFT)
        added_lbl_2.grid(row=0, column=1, pady=5)

        added_lbl_3 = tix.Label(register_window, text="Emphasis", justify=tix.LEFT)
        added_lbl_3.grid(row=0, column=2, pady=5)

        for pie_item in copy_pie_items:
            appended_lbl1 = tix.Label(register_window, text=f"{pie_item.title()}")
            appended_lbl1.grid(row=a + 1, column=0)

            appended_lbl2 = tix.Label(register_window, text=f"{copy_pie_items_percentage[a]}")
            appended_lbl2.grid(row=a + 1, column=1)

            if copy_explode[a] == 0.1:
                _explode_ = "Enabled"

            else:
                _explode_ = "Disabled"

            appended_lbl3 = tix.Label(register_window, text=f"{_explode_}")
            appended_lbl3.grid(row=a + 1, column=2)

            a += 1

        appended_lbl2.grid(pady=10)

    else:
        added_lbl_1 = tix.Label(register_window, text="No items added yet. Maybe add some items?")
        added_lbl_1.grid(row=0, column=1, pady=10)

    clear_register_btn = tix.Button(register_window, text="Clear Register", justify='center', bd=1, cursor='hand2', relief=tix.SOLID, command=lambda: _clear(register_window))
    clear_register_btn.grid(row=a + 1, column=1, pady=10)

    register_window.after(0, lambda: center_window(register_window, 'PCC Register'))
    register_window.protocol('WM_DELETE_WINDOW', lambda: _exit(register_window))
    register_window.mainloop()


def make_chart():
    '''Make pie-chart as per the user's data'''

    if pie_items:
        figure, pie_chart = plt.subplots()
        pie_chart.pie(pie_items_percentage, explode=explode, labels=pie_items, autopct='%1.2f%%', shadow=True, startangle=90)
        pie_chart.axis('equal')
        plt.show()

    else:
        messagebox.showerror('No data', 'No data were inputed to make pie-charts')


def _exit(_window):
    '''Destroy Tk window or Toplevel window'''

    if _window == window:
        if messagebox.askyesno('Exit', 'Do you really want to exit?'):
            window.destroy()

    else:
        _window.destroy()
        window.deiconify()


def _clear(_window=None):
    '''Clear data from the register'''

    if pie_items:
        if messagebox.askyesno('Clear Register?', 'Do you really want to clear REGISTER?', parent=_window):
            for lists in [pie_items, pie_items_percentage, explode]:
                lists.clear()

    else:
        messagebox.showinfo('Clear Register', "No items added yet. How about adding some items?", parent=_window)

    if _window:
        _exit(_window)


def left_button_bind(event=None):
    '''Focus out from the entry widget when user clicks to any widget'''

    if event.widget not in [item_entry, percentage_entry, explode_entry]:
        window.focus()


def resource_path(relative_path):
    '''Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


explode, pie_items, pie_items_percentage = [], [], []

window = tix.Tk()

screen_width, screen_height = window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2

for _ in range(8):
    window.columnconfigure(_, weight=1)
    window.rowconfigure(_, weight=1)

pcc_logo = tix.PhotoImage(file=resource_path('included_files\\PCC_Logo.png'))
pcc_logo_lbl = tix.Label(window, image=pcc_logo, cursor='hand2')
pcc_logo_lbl.grid(column=1, columnspan=3)
pcc_logo_lbl.bind('<Button-1>', open_link)

item_entry_lbl = tix.Label(window, text="Name of item:")
item_entry_lbl.grid(row=1, column=1, sticky="W")

item_entry = tix.Entry(window)
item_entry.grid(row=1, column=2, sticky="WE")

percentage_entry_lbl = tix.Label(window, text="Percentage:")
percentage_entry_lbl.grid(row=2, column=1, sticky="W")

percentage_entry = tix.Entry(window)
percentage_entry.grid(row=2, column=2, sticky="WE")

explode_entry_lbl = tix.Label(window, text="Enable emphasis(Y/N):")
explode_entry_lbl.grid(row=3, column=1, sticky="W")

explode_entry = tix.Entry(window)
explode_entry.grid(row=3, column=2, sticky="WE")

append_btn = tix.Button(window, text="Add values to register", cursor='hand2', command=append)
append_btn.grid(row=4, column=1, sticky="WE", columnspan=3, padx=1, pady=1)

show_register_btn = tix.Button(window, text="View register", cursor='hand2', command=show_register)
show_register_btn.grid(row=5, column=1, sticky="WE", columnspan=3, padx=1, pady=1)

clear_btn = tix.Button(window, text="Clear Register", cursor='hand2', command=_clear)
clear_btn.grid(row=6, column=1, sticky="WE", columnspan=3, padx=1, pady=1)

make_chart_btn = tix.Button(window, text="Make Pie-Chart", cursor='hand2', command=make_chart)
make_chart_btn.grid(row=7, column=1, columnspan=3, sticky="WE", padx=1, pady=1)

window.bind('<Button-1>', left_button_bind)
window.protocol('WM_DELETE_WINDOW', lambda: _exit(window))
window.after(0, lambda: center_window(window, 'Pie Chart Creator'))

balloon = tix.Balloon(window)
balloon.bind_widget(item_entry, balloonmsg='Input desire name for your item.')
balloon.bind_widget(clear_btn, balloonmsg='Clear ALL VALUES from the register.')
balloon.bind_widget(pcc_logo_lbl, balloonmsg='http://github.com/NMrocks/Pie-Chart-Creator')
balloon.bind_widget(show_register_btn, balloonmsg='View and Edit items stored in register.')
balloon.bind_widget(percentage_entry, balloonmsg='Input percentage for the name of your item.')
balloon.bind_widget(make_chart_btn, balloonmsg='Generate a pie-chart according to the data provided by you.')
balloon.bind_widget(append_btn, balloonmsg='Add values you have entered in the input fields to the register.')
balloon.bind_widget(explode_entry, balloonmsg="'Y' enables emphasis whereas 'N' disables it. If enabled some\nspaces will be created between the items in the pie-chart.")

window.mainloop()
