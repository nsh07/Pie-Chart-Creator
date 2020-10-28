'''
The GUI window when user clicks the view button
'''

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from data import tips
from data import commands
from data import include


class UI:
    def __init__(self, master, _vars):
        self._vars = _vars

        self.master = master
        self.master.withdraw()

        self.toplevel = tk.Toplevel(self.master)
        self.container_frame = tk.Frame(self.toplevel)
        self.tips = tips.Tips(self.toplevel)

        self.items_frame = tk.Frame(self.container_frame)
        self.items_label = tk.Label(self.items_frame, text='ITEMS')
        self.items_text_widget = tk.Text(self.items_frame, width=15, height=15, state='disabled', cursor='arrow')
        self.items_label.pack()
        self.items_text_widget.pack()
        self.items_frame.pack(side=tk.LEFT)

        self.value_frame = tk.Frame(self.container_frame)
        self.value_label = tk.Label(self.value_frame, text='VALUES')
        self.value_text_widget = tk.Text(self.value_frame, width=12, height=15, state='disabled', cursor='arrow')
        self.value_label.pack()
        self.value_text_widget.pack()
        self.value_frame.pack(side=tk.LEFT)

        self.explode_frame = tk.Frame(self.container_frame)
        self.explode_label = tk.Label(self.explode_frame, text='EXPLODE')
        self.explode_text_widget_frame = tk.Frame(self.explode_frame)
        self.explode_text_widget = tk.Text(self.explode_text_widget_frame, width=12, height=15, state='disabled', cursor='arrow')
        self.explode_label.pack()
        self.explode_text_widget.pack(side=tk.LEFT)
        self.explode_text_widget_frame.pack()
        self.explode_frame.pack(side=tk.LEFT)

        self.pie_text_widgets = [self.items_text_widget, self.value_text_widget, self.explode_text_widget]

        self.scrollbar = tk.Scrollbar(self.explode_text_widget_frame, orient="vertical", command=self.multiple_yview)
        self.scrollbar.pack(side=tk.LEFT, fill='y')

        for widgets in self.pie_text_widgets:
            widgets.config(yscrollcommand=self.scrollbar.set)

        self.container_frame.pack(padx=1)

        self.var = tk.IntVar()
        self.enable_editing_button = ttk.Checkbutton(self.toplevel, text='Enable Editing Mode', variable=self.var, cursor='hand2', command=self.enable_editing_command)
        self.enable_editing_button.pack(pady=10)

        self.tips.set_tips(self.enable_editing_button, 'Enable Editing Mode')
        self.tips.set_tips(self.items_text_widget, 'List of name of items')
        self.tips.set_tips(self.value_text_widget, 'List of the values of each items')
        self.tips.set_tips(self.explode_text_widget, 'List of enabled or disabled explode data of each items')

        self.toplevel.protocol('WM_DELETE_WINDOW', self.top_level_exit)
        self.toplevel.after(0, lambda: include.initial_position(self.toplevel, 'Register'))
        self.toplevel.after(0, lambda: commands.insert_to_text_widget(self.pie_text_widgets, _vars))
        self.toplevel.mainloop()

    def top_level_exit(self):
        '''When user clicks X button of the top-level window'''

        get_items = [item.strip() for item in self.items_text_widget.get('1.0', 'end-1c').split('\n') if item.strip()]
        get_values = [float(value.strip()) for value in self.value_text_widget.get('1.0', 'end-1c').split('\n') if value.strip()]
        get_explode = [0.1 if exp == 'Enabled' else 0 for exp in self.explode_text_widget.get('1.0', 'end-1c').split('\n') if exp in ['Enabled', 'Disabled']]

        if len(get_items) == len(get_values) == len(get_explode):  # If values in items, values and explode list is correctly inserted
            for index, _items in enumerate([get_items, get_values, get_explode]):
                self._vars[index].clear()
                self._vars[index].extend(_items)

            self.toplevel.destroy()
            self.master.deiconify()

        else:
            if messagebox.askyesno('Broken Details', 'Some values are missing either in ITEMS or in VALUES.\n\nYes = Delete all values you have entered \nNo = Manually edit missings values', parent=self.toplevel):
                for _var in self._vars:
                    _var.clear()

                self.toplevel.destroy()
                self.master.deiconify()

            else:
                self.var.set(1)
                self.enable_editing_command()
                messagebox.showinfo('Edit Mode', 'Editing Mode is Enabled')

    def enable_editing_command(self):
        '''When user clicks the enable editing checkbutton'''

        if self.var.get() == 1:
            for widget in self.pie_text_widgets:
                widget.config(state='normal', cursor='xterm')

        else:
            for widget in self.pie_text_widgets:
                widget.config(state='disabled', cursor='arrow')

    def multiple_yview(self, *args):
        '''Creating commands of y-view for  all the TEXT widget'''

        for widgets in self.pie_text_widgets:
            widgets.yview(*args)
