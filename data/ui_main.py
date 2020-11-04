'''
The main GUI window.
'''

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.tix as tix
from tkinter import messagebox
import tips
import link
import ui_view
import include
import commands


class UI:
    def __init__(self):
        self.explode, self.pie_items, self.pie_items_percentage = [], [], []

        self.master = tix.Tk()
        self.container_frame = tix.Frame(self.master, bg='white')
        self.tips = tips.Tips(self.master)

        self.image_frame = tix.Frame(self.container_frame)
        self.image_obj = tix.PhotoImage(file=include.resource_path('..\\pics\\PCC_Logo.png'))
        self.image_label = tix.Label(self.image_frame, image=self.image_obj, cursor='hand2')
        self.image_label.bind('<Button-1>', lambda e: link.open_link(self.master))
        self.image_label.pack()
        self.image_frame.pack()

        self.entries_frame = tix.Frame(self.container_frame, bg='white')
        self.items_style, self.value_style = ttk.Style(), ttk.Style()
        self.items_style.configure('I.TEntry', foreground='grey')
        self.value_style.configure('V.TEntry', foreground='grey')
        self.item_entry = ttk.Entry(self.entries_frame, justify=tix.CENTER, width=35, style='I.TEntry')
        self.value_entry = ttk.Entry(self.entries_frame, justify=tix.CENTER, width=35, style='V.TEntry')

        self.radio_button_style = ttk.Style()
        self.radio_button_style.configure('R.TRadiobutton', background='white')
        self.explode_frame = tk.LabelFrame(self.container_frame, text='Explode', bg='white')
        self.radio_button_var = tix.IntVar()
        self.explode_radio_button_enable = ttk.Radiobutton(self.explode_frame, text='Enable', variable=self.radio_button_var, value=1, cursor='hand2', style='R.TRadiobutton')
        self.explode_radio_button_disable = ttk.Radiobutton(self.explode_frame, text='Disable', variable=self.radio_button_var, value=2, cursor='hand2', style='R.TRadiobutton')
        self.explode_radio_button_enable.pack(side=tix.LEFT, ipadx=15, ipady=5)
        self.explode_radio_button_disable.pack(side=tix.LEFT)

        self.item_entry.pack(ipady=2, pady=5)
        self.value_entry.pack(ipady=2, pady=5)
        self.entries_frame.pack(pady=5)
        self.explode_frame.pack(ipady=2, pady=5)

        for widget, text in {self.item_entry: 'Items', self.value_entry: 'Values'}.items():
            widget.insert(tix.END, text)

        self.styles_list = {self.items_style: 'I.TEntry', self.value_style: 'V.TEntry'}
        self.pie_vars = (self.pie_items, self.pie_items_percentage, self.explode)
        self.pie_entries = (self.item_entry, self.value_entry, self.radio_button_var)

        self.buttons_frame = tix.Frame(self.container_frame, bg='white')
        self.add_value_button = tix.Button(self.buttons_frame, text='Add Values', bg='white', activebackground='white', cursor='hand2', relief=tix.GROOVE, command=lambda: commands.add_command(self.pie_entries, self.pie_vars, self.styles_list))
        self.view_button = tix.Button(self.buttons_frame, text='View Register', bg='white', activebackground='white', cursor='hand2', relief=tix.GROOVE, command=lambda: ui_view.UI(self.master, self.pie_vars))
        self.clear_button = tix.Button(self.buttons_frame, text='Clear Register', bg='white', activebackground='white', cursor='hand2', relief=tix.GROOVE, command=lambda: commands.clear(self.pie_vars, self.pie_entries, self.styles_list))
        self.make_pie_chart_button = tix.Button(self.buttons_frame, text='Make Pie-Chart', bg='white', activebackground='white', cursor='hand2', relief=tix.GROOVE, command=lambda: commands.make_chart(self.pie_vars))

        self.add_value_button.pack(ipadx=71, ipady=2, pady=3)
        self.view_button.pack(ipadx=65, ipady=2, pady=3)
        self.clear_button.pack(ipadx=64, ipady=2, pady=3)
        self.make_pie_chart_button.pack(ipadx=59, ipady=2, pady=3)

        self.buttons_frame.pack()

        self.tips.set_tips(self.item_entry, 'Input desire name for your item.')
        self.tips.set_tips(self.clear_button, 'Clear ALL VALUES from the register.')
        self.tips.set_tips(self.view_button, 'View and Edit items stored in register.')
        self.tips.set_tips(self.image_label, 'http://github.com/NMrocks/Pie-Chart-Creator')
        self.tips.set_tips(self.value_entry, 'Input values for the name of your item.')
        self.tips.set_tips(self.explode_frame, 'Explode is spliting some part of pie-chart if Enabled')
        self.tips.set_tips(self.add_value_button, 'Add values you have entered in the input fields to the register.')
        self.tips.set_tips(self.make_pie_chart_button, 'Generate a pie-chart according to the data provided by you.')

        self.master.after(0, lambda: include.initial_position(self.master, 'Pie Chart Creator'))
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.bind('<Button-1>', self.master_bindings)
        self.item_entry.bind('<FocusIn>', self.entry_bindings)
        self.value_entry.bind('<FocusIn>', self.entry_bindings)
        self.explode_radio_button_enable.bind('<FocusIn>', self.entry_bindings)

        self.container_frame.pack()
        self.master.mainloop()

    def master_bindings(self, event=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        widget = event.widget
        widgets = [self.item_entry, self.value_entry]
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'), self.value_entry: (self.value_style, 'V.TEntry')}

        for wid in entries_widgets:
            if not wid.get().strip():
                wid.delete(0, tix.END)
                wid.insert(tix.END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

        if widget not in widgets:
            self.master.focus()

    def entry_bindings(self, event=None):
        '''When user clicks in or out of the entries widget'''

        widget = event.widget
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'), self.value_entry: (self.value_style, 'V.TEntry')}

        if widget in entries_widgets:
            if widget.get().strip() == entries_widgets[widget]:
                widget.delete(0, tix.END)
                style, style_name = entries_styles[widget]
                style.configure(style_name, foreground='black')

                entries_widgets.pop(widget)
                entries_styles.pop(widget)

        for wid in entries_widgets:
            if not wid.get().strip():
                wid.delete(0, tix.END)
                wid.insert(tix.END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

    def exit(self):
        '''When user clicks to X button in the title bar'''

        if messagebox.askyesno('Exit', 'Do you really want to exit?', parent=self.master):
            self.master.destroy()
