'''
The main GUI window.
'''

import tkinter as tk
import tkinter.ttk as ttk
import link
import include
import commands


class UI:
    def __init__(self):
        self.prev_widget = None
        self.master = tk.Tk()
        self.left_frame = tk.Frame(self.master, bg='white')

        self.image_frame = tk.Frame(self.left_frame, bg='white')
        self.image_obj = tk.PhotoImage(file=include.resource_path('PCC_Logo.png'))
        self.image_label = tk.Label(self.image_frame, image=self.image_obj, cursor='hand2', bg='white')
        self.image_label.bind('<Button-1>', lambda e: link.open_link(self.master))
        self.image_label.pack()
        self.image_frame.pack()

        self.entries_frame = tk.Frame(self.left_frame, bg='white')
        self.items_style, self.value_style = ttk.Style(), ttk.Style()
        self.items_style.configure('I.TEntry', foreground='grey')
        self.value_style.configure('V.TEntry', foreground='grey')
        self.item_entry = ttk.Entry(self.entries_frame, justify=tk.CENTER, width=35, style='I.TEntry')
        self.value_entry = ttk.Entry(self.entries_frame, justify=tk.CENTER, width=35, style='V.TEntry')

        self.radio_button_style = ttk.Style()
        self.radio_button_style.configure('R.TRadiobutton', background='white')
        self.explode_frame = tk.LabelFrame(self.left_frame, text='Explode', bg='white')
        self.radio_button_var = tk.IntVar()
        self.explode_radio_button_enable = ttk.Radiobutton(self.explode_frame, text='Enable', variable=self.radio_button_var, value=1, cursor='hand2', style='R.TRadiobutton')
        self.explode_radio_button_disable = ttk.Radiobutton(self.explode_frame, text='Disable', variable=self.radio_button_var, value=2, cursor='hand2', style='R.TRadiobutton')
        self.explode_radio_button_enable.pack(side=tk.LEFT, ipadx=15, ipady=5)
        self.explode_radio_button_disable.pack(side=tk.LEFT)

        self.item_entry.pack(ipady=2, pady=3)
        self.value_entry.pack(ipady=2, pady=3)
        self.entries_frame.pack(pady=3)
        self.explode_frame.pack(ipady=2, pady=3)

        for widget, text in {self.item_entry: 'Items', self.value_entry: 'Values'}.items():
            widget.insert(tk.END, text)

        self.styles_list = {self.items_style: 'I.TEntry', self.value_style: 'V.TEntry'}
        self.pie_entries = (self.item_entry, self.value_entry, self.radio_button_var)

        self.buttons_frame = tk.Frame(self.left_frame, bg='white')
        self.add_value_button = tk.Button(self.buttons_frame, text='Add Values', bg='white', activebackground='white', cursor='hand2', relief=tk.GROOVE, command=lambda: commands.add_command(self.pie_entries, self.text_widgets, self.styles_list))
        self.clear_button = tk.Button(self.buttons_frame, text='Clear Register', bg='white', activebackground='white', cursor='hand2', relief=tk.GROOVE, command=lambda: commands.clear(self.text_widgets))
        self.make_pie_chart_button = tk.Button(self.buttons_frame, text='Make Pie-Chart', bg='white', activebackground='white', cursor='hand2', relief=tk.GROOVE, command=lambda: commands.make_chart(self.text_widgets))

        self.add_value_button.pack(ipadx=71, ipady=2, pady=3)
        self.clear_button.pack(ipadx=64, ipady=2, pady=3)
        self.make_pie_chart_button.pack(ipadx=59, ipady=2, pady=3)

        self.buttons_frame.pack()

        self.right_frame = tk.Frame(self.master, bg='white')
        self.register_frame = tk.Frame(self.right_frame, bg='white')

        self.items_ = Widgets(self.register_frame, 'ITEMS', 15)
        self.values_ = Widgets(self.register_frame, 'VALUES')
        self.explode_ = Widgets(self.register_frame, 'EXPLODE')

        self.text_widgets = [self.items_.text_widget, self.values_.text_widget, self.explode_.text_widget]

        self.scrollbar = tk.Scrollbar(self.explode_.text_widget_frame, orient="vertical", command=self.multiple_yview)
        self.scrollbar.pack(side=tk.LEFT, fill='y')

        for widgets in self.text_widgets:
            widgets.config(yscrollcommand=self.scrollbar.set)

        self.register_frame.pack()

        self.var = tk.IntVar()
        self.checkbutton_style = ttk.Style()
        self.checkbutton_style.configure('CH.TCheckbutton', background='white')
        self.button_frame = tk.Frame(self.right_frame, bg='white')
        self.enable_editing_button = ttk.Checkbutton(self.button_frame, text='Enable Editing Mode', variable=self.var, cursor='hand2', style='CH.TCheckbutton', command=self.enable_editing_command)
        self.enable_editing_button.pack(pady=10)
        self.button_frame.pack()

        self.master.bind('<Button-1>', self.master_bindings)
        self.item_entry.bind('<FocusIn>', self.entry_bindings)
        self.value_entry.bind('<FocusIn>', self.entry_bindings)
        self.explode_radio_button_enable.bind('<FocusIn>', self.entry_bindings)
        self.master.after(0, lambda: include.initial_position(self.master, 'Pie Chart Creator'))

        # Showing url when hovered to image and removing it after 250 ms when cursor gets removed from the top of image
        self.url_label = tk.Label(self.master, text='http://github.com/NMrocks/Pie-Chart-Creator', fg='green')
        self.image_frame.bind('<Enter>', lambda e: self.url_label.place(relx=0, x=10, y=105, rely=0))
        self.image_frame.bind('<Leave>', lambda e: self.master.after(250, self.url_label.place_forget()))

        self.left_frame.pack(side=tk.LEFT)
        self.right_frame.pack(padx=1, side=tk.LEFT)
        self.master.config(bg='white')
        self.master.mainloop()

    def master_bindings(self, event=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        widget = event.widget
        widgets = [self.item_entry, self.value_entry]
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'), self.value_entry: (self.value_style, 'V.TEntry')}

        for wid in entries_widgets:
            if not wid.get().strip() and widget != self.prev_widget:
                wid.delete(0, tk.END)
                wid.insert(tk.END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

        if widget not in widgets:
            if isinstance(widget, tk.Text) and widget.cget('state') == 'normal':
                return

            self.master.focus()

    def entry_bindings(self, event=None):
        '''When user clicks in or out of the entries widget'''

        widget = event.widget
        entries_widgets = {self.item_entry: 'Items', self.value_entry: 'Values'}
        entries_styles = {self.item_entry: (self.items_style, 'I.TEntry'), self.value_entry: (self.value_style, 'V.TEntry')}

        if widget in entries_widgets:
            if widget.get().strip() == entries_widgets[widget]:
                self.prev_widget = widget
                widget.delete(0, tk.END)
                style, style_name = entries_styles[widget]
                style.configure(style_name, foreground='black')

                entries_widgets.pop(widget)
                entries_styles.pop(widget)

        for wid in entries_widgets:
            if not wid.get().strip():
                wid.delete(0, tk.END)
                wid.insert(tk.END, entries_widgets[wid])
                style, style_name = entries_styles[wid]
                style.configure(style_name, foreground='grey')

    def enable_editing_command(self):
        '''When user clicks the enable editing checkbutton'''

        if self.var.get() == 1:
            for widget in self.text_widgets:
                widget.config(state='normal', cursor='xterm')

        else:
            for widget in self.text_widgets:
                widget.config(state='disabled', cursor='arrow')

    def multiple_yview(self, *args):
        '''Creating commands of y-view for  all the TEXT widget'''

        for widgets in self.text_widgets:
            widgets.yview(*args)


class Widgets:
    def __init__(self, frame, value, width=12):
        self.frame = tk.Frame(frame, bg='white')
        self.label = tk.Label(self.frame, text=value, bg='white')
        self.text_widget_frame = tk.Frame(self.frame, bg='white')

        if not width:
            width = 15

        self.text_widget = tk.Text(self.text_widget_frame, width=width, height=19, highlightthickness=1,
                                   highlightbackground="silver", highlightcolor="silver", cursor='arrow', state='disabled')

        self.label.pack()
        self.text_widget_frame.pack()
        self.frame.pack(side=tk.LEFT)
        self.text_widget.pack(side=tk.LEFT)


if __name__ == '__main__':
    UI()
