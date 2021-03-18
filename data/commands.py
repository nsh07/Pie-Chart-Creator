'''
Different commands when user clicks different button
'''


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


def add_command(entry_widgets, text_widgets, styles):
    '''Store item_name, values and explode in respective variables'''

    entry_get = entry_widgets[0].get().strip()
    values_get = entry_widgets[1].get().strip()
    split_value_get = values_get.split('.')
    explode_get = entry_widgets[2].get()

    if entry_get in ['', 'Items']:
        messagebox.showerror('Invalid Name', 'Provide valid item name')

    elif entry_get in text_widgets[0].get('1.0', 'end-2c').split('\n'):
        messagebox.showerror('Exists', f'{entry_get} already exists in the register')

    elif values_get in ['', 'Values'] or not split_value_get[0].isdigit() or (len(split_value_get) == 2 and not split_value_get[1].isdigit()):
        messagebox.showerror('Invalid Values', 'Values was expected in number')

    elif explode_get not in [1, 2]:
        messagebox.showerror('Invalid Explode', 'You must select Enable or Disable in Explode option')

    else:
        default_state(entry_widgets, styles)
        insert_to_text_widget(text_widgets, entry_get, values_get, explode_get)


def insert_to_text_widget(text_widgets, *values):
    '''Inserting data from self.explode, self.pie_items and self.pie_items_values in their own text_widget'''

    pie_items = text_widgets[0].get('1.0', 'end-1c') + values[0]
    pie_values = text_widgets[1].get('1.0', 'end-1c') + values[1]
    pie_explode = text_widgets[2].get('1.0', 'end-1c')

    if values[2] == 1:
        pie_explode += 'Enabled'

    else:
        pie_explode += 'Disabled'

    for widget in text_widgets:
        widget.config(state='normal')
        widget.delete('1.0', 'end')

    text_widgets[0].insert('1.0', f'{pie_items}\n')
    text_widgets[1].insert('1.0', f'{pie_values}\n')
    text_widgets[2].insert('1.0', f'{pie_explode}\n')

    for widget in text_widgets:
        widget.config(state='disabled', cursor='arrow')


def make_chart(text_widgets):
    '''Make pie-chart as per the user's data'''

    items = text_widgets[0].get('1.0', 'end-2c').split('\n')
    values = [float(value) for value in text_widgets[1].get('1.0', 'end-2c').split('\n') if value]
    explode = [0.1 if value == 'Enabled' else 0 for value in text_widgets[2].get('1.0', 'end-2c').split('\n')]

    if len(items) != len(values) != len(explode):
        messagebox.showerror('ERROR', 'There is incomplete values either in ITEMS or VALUES or EXPLODE')

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


def clear(text_widgets):
    '''Clear data from the register'''

    if messagebox.askyesno('Clear Register?', 'Do you really want to clear REGISTER?'):
        for widget in text_widgets:
            widget.config(state='normal')
            widget.delete('1.0', 'end')
            widget.config(state='disabled')

        messagebox.showinfo('Cleared', 'All values are cleared from the REGISTER')
