'''
Different commands when user clicks different button
'''


import collections
from tkinter import messagebox
import matplotlib.pyplot as plt


def default_state(entry_widgets, styles):
    '''Set the entries box and radio-button the default state after adding the value'''

    for widget, text in {entry_widgets[0]: 'Items', entry_widgets[1]: 'Values'}.items():
        widget.delete(0, 'end')
        widget.insert('end', text)

    for style, name in styles.items():  # Change the foreground color of entries box
        style.configure(name, foreground='grey')

    entry_widgets[2].set(0)


def add_command(entry_widgets, _vars, styles):
    '''Store item_name, values and explode in respective variables'''

    entry_get = entry_widgets[0].get().strip()
    values_get = entry_widgets[1].get().strip()
    split_value_get = values_get.split('.')
    explode_get = entry_widgets[2].get()

    pie_items_var, values_var, explode_var = _vars

    if entry_get in ['', 'Items']:
        messagebox.showerror('Invalid Name', 'Provide valid item name')

    elif entry_get in _vars[0]:
        messagebox.showerror('Exists', f'{entry_get} already exists in the register')

    elif not split_value_get[0].isdigit() and not split_value_get[1].isdigit():
        messagebox.showerror('Invalid Values', 'Values was expected in number')

    elif explode_get not in [1, 2]:
        messagebox.showerror('Invalid Explode', 'You must select Enable or Disable in Explode option')

    else:
        pie_items_var.append(entry_get)
        values_var.append(float(values_get))

        if explode_get == 1:
            explode_var.append(0.1)

        else:
            explode_var.append(0)

        messagebox.showinfo('Added', 'Values are added')
        default_state(entry_widgets, styles)


def insert_to_text_widget(text_widgets, _vars):
    '''Inserting data from self.explode, self.pie_items and self.pie_items_values in their own text_widget'''

    for widget in text_widgets:
        widget.config(state='normal')
        widget.delete('1.0', 'end')

    pie_items, pie_values, pie_explode = _vars
    pie_explode = ['Enabled' if explode else 'Disabled' for explode in pie_explode]

    for index, values in enumerate(zip(pie_items, pie_values, pie_explode)):
        item, values, explode = values

        text_widgets[0].insert('1.0', f'{item}\n')
        text_widgets[1].insert('1.0', f'{values}\n')
        text_widgets[2].insert('1.0', f'{explode}\n')

    for widget in text_widgets:
        widget.config(state='disabled', cursor='arrow')


def make_chart(_vars):
    '''Make pie-chart as per the user's data'''

    items, values, explode = _vars
    count = len(set(collections.Counter(items).values()))  # Getting count of items and calculating its length

    if count > 1:
        messagebox.showerror('ERROR', 'Some items have same names.')

    elif items:
        figure, pie_chart = plt.subplots()

        if messagebox.askyesno('Shadow', 'Do you want to show in your pie-chart?'):
            pie_chart.pie(values, explode=explode, labels=items, autopct='%1.2f%%', shadow=True, startangle=90)

        else:
            pie_chart.pie(values, explode=explode, labels=items, autopct='%1.2f%%', shadow=False, startangle=90)

        pie_chart.axis('equal')
        plt.show()

    else:
        messagebox.showerror('No data', 'No data were inputed to make pie-charts')


def clear(_vars, text_widgets=None, styles=None):
    '''Clear data from the register'''

    if _vars[0]:
        if messagebox.askyesno('Clear Register?', 'Do you really want to clear REGISTER?'):
            for _var in _vars:
                _var.clear()

            messagebox.showinfo('Cleared', 'All values are cleared from the REGISTER')
            default_state(text_widgets, styles)

    else:
        messagebox.showinfo('Clear Register', "No items added yet. How about adding some items?")