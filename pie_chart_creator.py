import os
import sys

try:  # Python 3
    import tkinter as tk
    from tkinter import messagebox

except (ModuleNotFoundError, ImportError):  # Python 2
    import Tkinter as tk
    import tkMessageBox as messagebox

import matplotlib.pyplot as plt


def center_window(window, title):
    '''This function places any window (either TopLevel or Tk) to the center of the screen'''

    window.withdraw()

    window.update()
    window.focus()
    window.grab_set()
    window.title(title)
    window.resizable(0, 0)
    window.iconbitmap(resource_path('included_files\\icon.ico'))

    width, height = window.winfo_width(), window.winfo_height()
    window.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')
    window.deiconify()


def change_style(wid):
    '''Change text styles to bold or italic'''

    italic_index = ('23.0', '23.83')
    bold_indexs = [('1.0', '1.19'), ('4.0', '4.14'), ('5.4', '5.31'), ('8.4', '8.22'), ('11.4', '11.23'), ('14.4', '14.31'), ('17.4', '17.26'), ('20.4', '20.42')]

    for start, end in bold_indexs:
        wid.tag_add('b', start, end)

    wid.tag_configure('b', font=('Helvetica', '11', 'bold'))

    wid.tag_add('i', italic_index[0], italic_index[1])
    wid.tag_configure('i', font=('Helvetica', '11', 'italic'))

    wid.config(state=tk.DISABLED)


def instructions():
    '''Show instruction window'''

    file_path = resource_path('included_files\\instructions.txt')

    with open(file_path, 'r') as f:
        contents = f.read().strip('\n')

    instructions_window = tk.Toplevel(window)

    instructions_text_widget_frame = tk.Frame(instructions_window)

    instructions_text_widget = tk.Text(instructions_text_widget_frame, height=26, cursor='arrow')
    instructions_text_widget.insert('1.0', contents)
    instructions_text_widget.pack(side=tk.LEFT)

    instructions_text_widget_frame.pack()

    instructions_window.after(0, lambda: change_style(instructions_text_widget))
    instructions_window.after(0, lambda: center_window(instructions_window, 'PCC Instructions'))
    instructions_window.mainloop()


def append():
    '''Store data given by the user'''

    item = item_entry.get().title()
    explode_ = explode_entry.get().title()
    percentage = percentage_entry.get()

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
            widget.delete(0, tk.END)

    else:
        messagebox.showerror('Invalid Percentage', 'Percentage must be in number')


def show_register():
    '''Show stored data'''

    copy_pie_items = pie_items
    copy_pie_items_percentage = pie_items_percentage
    copy_explode = explode

    a = 0

    register_window = tk.Toplevel()

    if pie_items:
        added_lbl_1 = tk.Label(register_window, text="Name of item", justify=tk.LEFT)
        added_lbl_1.grid(row=0, column=0, pady=5)

        added_lbl_2 = tk.Label(register_window, text="Percentage", justify=tk.LEFT)
        added_lbl_2.grid(row=0, column=1, pady=5)

        added_lbl_3 = tk.Label(register_window, text="Emphasis", justify=tk.LEFT)
        added_lbl_3.grid(row=0, column=2, pady=5)

        for pie_item in copy_pie_items:
            appended_lbl1 = tk.Label(register_window, text=f"{pie_item.title()}")
            appended_lbl1.grid(row=a + 1, column=0)

            appended_lbl2 = tk.Label(register_window, text=f"{copy_pie_items_percentage[a]}")
            appended_lbl2.grid(row=a + 1, column=1)

            if copy_explode[a] == 0.1:
                _explode_ = "Enabled"

            else:
                _explode_ = "Disabled"

            appended_lbl3 = tk.Label(register_window, text=f"{_explode_}")
            appended_lbl3.grid(row=a + 1, column=2)

            a += 1

        appended_lbl2.grid(pady=10)

    else:
        added_lbl_1 = tk.Label(register_window, text="No items added yet. Maybe add some items?")
        added_lbl_1.grid(row=0, column=1, pady=10)

    clear_register_btn = tk.Button(register_window, text="Clear Register", justify='center', bd=1, cursor='hand2', relief=tk.SOLID, command=lambda: clear(register_window))
    clear_register_btn.grid(row=a + 1, column=1, pady=10)

    register_window.after(0, lambda: center_window(register_window, 'PCC Register'))
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


def _exit_():
    '''Quit program'''

    if messagebox.askyesno('Exit?', 'Do you really want to exit?\nAll registered values will be lost'):
        window.destroy()


def clear(window=None):
    '''Clear data from the register'''

    if pie_items:
        if messagebox.askyesno('Clear Register?', 'Do you really want to clear REGISTER?'):
            for lists in [pie_items, pie_items_percentage, explode]:
                del lists[0]

    else:
        messagebox.showinfo('Clear Register?', "No items added yet. Maybe add some items?")

    if window:
        window.destroy()


def left_button_bind(event, window):
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

window = tk.Tk()
screen_width, screen_height = window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2

for _ in range(8):
    window.columnconfigure(_, weight=1)
    window.rowconfigure(_, weight=1)

pcc_logo = tk.PhotoImage(file=resource_path('included_files\\PCC_Logo.png'))
pcc_logo_lbl = tk.Label(window, image=pcc_logo)
pcc_logo_lbl.grid(column=1, columnspan=3)

item_entry_lbl = tk.Label(window, text="Name of item:")
item_entry_lbl.grid(row=1, column=1, sticky="W")

item_entry = tk.Entry(window)
item_entry.grid(row=1, column=2, sticky="WE")

percentage_entry_lbl = tk.Label(window, text="Percentage:")
percentage_entry_lbl.grid(row=2, column=1, sticky="W")

percentage_entry = tk.Entry(window)
percentage_entry.grid(row=2, column=2, sticky="WE")

explode_entry_lbl = tk.Label(window, text="Enable emphasis(Y/N):")
explode_entry_lbl.grid(row=3, column=1, sticky="W")

explode_entry = tk.Entry(window)
explode_entry.grid(row=3, column=2, sticky="WE")

append_btn = tk.Button(window, text="Add values to register", command=append)
append_btn.grid(row=4, column=1, sticky="WE", padx=1, pady=1)

make_chart_btn = tk.Button(window, text="Make chart with registered values", command=make_chart)
make_chart_btn.grid(row=7, column=1, columnspan=2, sticky="WE", padx=1, pady=1)

clear_btn = tk.Button(window, text="Clear Register", command=clear)
clear_btn.grid(row=5, column=1, sticky="WE", padx=1, pady=1)

exit_btn = tk.Button(window, text="Exit Pie Chart Creator", command=_exit_)
exit_btn.grid(row=5, column=2, sticky="WE", padx=1, pady=1)

show_register_btn = tk.Button(window, text="View register", command=show_register)
show_register_btn.grid(row=4, column=2, sticky="WE", padx=1, pady=1)

instructions_btn = tk.Button(window, text="Read Instructions", command=instructions)
instructions_btn.grid(row=6, column=1, columnspan=2, sticky="WE", padx=1, pady=1)

window.bind('<Button-1>', lambda event, window=window: left_button_bind(event, window))
window.after(0, lambda: center_window(window, 'Pie Chart Creator'))
window.mainloop()
