
# This program can be used, but some features aren't completely ready yet. I'll update this soon to fix all bugs.
import matplotlib.pyplot as plt
import tkinter as tk


class Check:  # Simple class to check if a value is float, yes etc.
	def __init__(self, string):
		self.string = string

	def isyes(self):
		if self.string.title() == "Y" or self.string.title() == "Yes":
			return True
		else:
			return False

	def isfloat(self):
		if self.string.replace(".", "", 1).isdigit():
			return True
		else:
			return False


window = tk.Tk()

pcc_logo = tk.PhotoImage(file="PCC_Logo.png")
pcc_logo_lbl = tk.Label(window, image=pcc_logo)
pcc_logo_lbl.grid(column=1, columnspan=3)

pie_items = []
pie_items_percentage = []
explode = []


def append():
	def exit_not_appended():
		not_appended.destroy()

	if Check.isfloat(Check(percentage_entry.get())):
		item = str(item_entry.get())
		pie_items.append(item.title())
		percentage = float(percentage_entry.get())
		pie_items_percentage.append(float(percentage).__round__(2))
		explode_ = explode_entry.get()
		if Check.isyes(Check(explode_)):
			explode.append(0.1)
		else:
			explode.append(0)

		item_entry.delete(0, tk.END)
		percentage_entry.delete(0, tk.END)
		explode_entry.delete(0, tk.END)

	else:
		not_appended = tk.Tk()
		not_appended_label = tk.Label(
			master=not_appended,
			text=f"Values not added to register\nbecause {percentage_entry.get()} is not a\nvalid decimal number.\nPress any key to exit this\nwarning menu."
		)
		not_appended_label.bind('<KeyPress>', exit_not_appended)
		not_appended_label.pack()


def show_register():
	copy_pie_items = pie_items
	copy_pie_items_percentage = pie_items_percentage
	copy_explode = explode
	register_window = tk.Tk()

	def exit_register():
		register_window.destroy()

	a, b = 0, 0
	if len(pie_items) != 0:
		added_lbl_1 = tk.Label(master=register_window, text="Name of item")
		added_lbl_2 = tk.Label(master=register_window, text="Percentage")
		added_lbl_3 = tk.Label(master=register_window, text="Emphasis")
		added_lbl_1.grid(row=0, column=1, sticky="W", pady=10)
		added_lbl_2.grid(row=0, column=2, padx=50, pady=10)
		added_lbl_3.grid(row=0, column=3, sticky="E", pady=10)

		for pie_item in copy_pie_items:
			appended_lbl1 = tk.Label(master=register_window, text=f"{pie_item.title()}")
			appended_lbl1.grid(row=a + 1, column=1, sticky="W")
			appended_lbl2 = tk.Label(master=register_window, text=f"{copy_pie_items_percentage[a]}")
			appended_lbl2.grid(row=a + 1, column=2)
			if copy_explode[b] == 0.1:
				_explode_ = "Enabled"
			else:
				_explode_ = "Disabled"
			appended_lbl3 = tk.Label(master=register_window, text=f"{_explode_}")
			appended_lbl3.grid(row=a + 1, column=3, sticky="E")

			a += 1
			b += 1

	else:
		added_lbl_1 = tk.Label(master=register_window, text="No items added yet. Maybe add some items?")
		added_lbl_1.grid(row=0, column=1, pady=10)

	exit_register_btn = tk.Button(
		master=register_window,
		text="Back to Pie Chart Creator",
		command=exit_register,
		)
	clear_register_btn = tk.Button(
			master=register_window,
			text="Clear Register",
			command=clear
			)
	exit_register_btn.grid(row=a + 1, column=1, columnspan=2, sticky="WE", padx=1, pady=1)
	clear_register_btn.grid(row=a + 1, column=3, sticky="WE", padx=1, pady=1)


def make_chart():
	figure, pie_chart = plt.subplots()
	pie_chart.pie(pie_items_percentage, explode=explode, labels=pie_items, autopct='%1.2f%%', shadow=True,
															startangle=90)
	pie_chart.axis('equal')
	plt.show()


def _exit_():
	def finalise_exit():
		exit_window.destroy()
		window.destroy()

	def cancel_exit():
		exit_window.destroy()

	exit_window = tk.Tk()
	exit_warning_lbl = tk.Label(master=exit_window, text="Do you really want to exit?\nAll registered values will be lost")
	exit_yes_btn = tk.Button(master=exit_window, text="Yes", command=finalise_exit)
	exit_no_btn = tk.Button(master=exit_window, text="No", command=cancel_exit)
	exit_warning_lbl.grid(row=1, column=1, columnspan=2, rowspan=2)
	exit_yes_btn.grid(row=3, column=1, sticky="WE", padx=1, pady=1)
	exit_no_btn.grid(row=3, column=2, sticky="WE", padx=1, pady=1)


def clear():
	clear_warning = tk.Tk()

	def finalise_clear():
		len_pie_items = len(pie_items)
		for _ in range(len_pie_items):
			del pie_items[0]
			del pie_items_percentage[0]
			del explode[0]
		clear_warning.destroy()

	def back_to_pcc():
		clear_warning.destroy()

	if len(pie_items) != 0:
		clear_warning_lbl = tk.Label(
					master=clear_warning,
					text="If you press the clear register button, all the\nvalues in the item register will be cleared.\nIt is advised to have a look at the register before clearing it.\nThis cannot be undone.",
					)
		clear_warning_lbl.grid(row=1, column=1, columnspan=2, pady=10)
		finalise_clear_btn = tk.Button(master=clear_warning, text="Clear Register", command=finalise_clear)
		finalise_clear_btn.grid(row=2, column=1, columnspan=2, sticky="WE", padx=1, pady=1)
		back_to_pcc_button = tk.Button(master=clear_warning, text="Back to Pie Chart Creator", command=back_to_pcc)
		back_to_pcc_button.grid(row=3, column=1, sticky="WE", padx=1, pady=1)
		view_register = tk.Button(master=clear_warning, text="View Register", command=show_register)
		view_register.grid(row=3, column=2, sticky="WE", padx=1, pady=1)

	else:
		added_lbl_1 = tk.Label(master=clear_warning, text="No items added yet. Maybe add some items?")
		added_lbl_1.grid(row=0, column=1, pady=10)
		exit_clear_warning = tk.Button(
			master=clear_warning,
			text="Back to Pie Chart Creator",
			command=back_to_pcc,
			)
		exit_clear_warning.grid(row=1, column=1, sticky="WE", padx=1, pady=1)


item_entry_lbl = tk.Label(text="Name of item:")
item_entry = tk.Entry()

item_entry_lbl.grid(row=1, column=1, sticky="W")
item_entry.grid(row=1, column=2, columnspan=2, sticky="WE")

percentage_entry_lbl = tk.Label(text="Percentage:")
percentage_entry = tk.Entry()

percentage_entry_lbl.grid(row=2, column=1, sticky="W")
percentage_entry.grid(row=2, column=2, columnspan=2, sticky="WE")

explode_entry_lbl = tk.Label(text="Enable emphasis(Y/N):")
explode_entry = tk.Entry()

explode_entry_lbl.grid(row=3, column=1, sticky="W")
explode_entry.grid(row=3, column=2, columnspan=2, sticky="WE")

append_btn = tk.Button(
	text="Add values to register",
	command=append
)
make_chart_btn = tk.Button(
	text="Make chart with registered values",
	command=make_chart
)
clear_btn = tk.Button(
	text="Clear Register",
	command=clear
)
exit_btn = tk.Button(
	text="Exit Pie Chart Creator",
	command=_exit_
)
show_register_btn = tk.Button(
	text="View register",
	command=show_register
)

append_btn.grid(row=4, column=1, sticky="WE", padx=1, pady=1)
show_register_btn.grid(row=4, column=2, columnspan=2, sticky="WE", padx=1, pady=1)
clear_btn.grid(row=5, column=1, sticky="WE", padx=1, pady=1)
exit_btn.grid(row=5, column=2, columnspan=2, sticky="WE", padx=1, pady=1)
make_chart_btn.grid(row=6, column=1, columnspan=3, sticky="WE", padx=1, pady=1)

window.mainloop()
