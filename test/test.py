import os
import sys
import time
import threading
from tkinter import *
import pyautogui as pyg


path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(1, path)

from Pie_Chart_Creator import PieCharCreator as PCC


def exit(event=None):
    thread.cancel()
    win.destroy()


def Test():
    # Below commented lines were used for recording purpose
    # pyg.click(917, 0)
    # pyg.click(646, 367)

    win.update()

    win_x, win_y = win.winfo_x(), win.winfo_y()

    item_x, item_y = pcc.item_entry.winfo_rootx(), pcc.item_entry.winfo_rooty()
    item_w, item_h = pcc.item_entry.winfo_width() // 2, pcc.item_entry.winfo_height() // 2
    item_final_x, item_final_y = item_x + item_w, item_y + item_h

    value_x, value_y = pcc.value_entry.winfo_rootx(), pcc.value_entry.winfo_rooty()
    value_w, value_h = pcc.value_entry.winfo_reqwidth() // 2, pcc.value_entry.winfo_reqheight() // 2
    value_final_x, value_final_y = value_x + value_w, value_y + value_h

    enable_x, enable_y = pcc.enable_radio.winfo_rootx(), pcc.enable_radio.winfo_rooty()
    enable_w, enable_h = pcc.enable_radio.winfo_reqwidth() // 2, pcc.enable_radio.winfo_reqheight() // 2
    enable_final_x, enable_final_y = enable_x + enable_w, enable_y + enable_h

    disable_x, disable_y = pcc.disable_radio.winfo_rootx(), pcc.disable_radio.winfo_rooty()
    disable_w, disable_h = pcc.disable_radio.winfo_reqwidth() // 2, pcc.disable_radio.winfo_reqheight() // 2
    disable_final_x, disable_final_y = disable_x + disable_w, disable_y + disable_h

    button_x, button_y = pcc.add_button.winfo_rootx(), pcc.add_button.winfo_rooty()
    button_w, button_h = pcc.add_button.winfo_width() // 2, pcc.add_button.winfo_reqheight() // 2
    button_final_x, button_final_y = button_x + button_w, button_y + button_h

    tups = [(item_final_x, item_final_y), (value_final_x, value_final_y),
            [(enable_final_x, enable_final_y), (disable_final_x, disable_final_y)],
            (button_final_x, button_final_y)]

    values = list(plotting_values.keys())

    for value in values:
        for idx, tup in enumerate(tups):
            explode = plotting_values[value][1]

            if idx == 2:
                if explode == 0.1:
                    tup = tup[0]

                else:
                    tup = tup[1]

            x, y = tup
            pyg.moveTo(x, y, duration=0.3)
            pyg.click(x, y)

            if idx == 0:
                pyg.write(str(value), 0.04)

            elif idx == 1:
                pyg.write(str(plotting_values[value][0]), 0.04)

    x, y = win_x, win_y

    for i in range(2):
        bbox = pcc.Tree.bbox(pcc.Tree.get_children()[0])

        _y = 80
        _x = x + bbox[2]

        pyg.moveTo(_x, _y, duration=0.3)
        pyg.click(button='right')

        _x += 10

        if i == 0:
            _y += 5

        else:
            _y += 20

        pyg.moveTo(_x + 10, _y + 5, duration=0.3)
        pyg.click(button='left')

    # time.sleep(0.5)
    # pyg.click(917, 0)
    # pyg.click(646, 367)


plotting_values = {'Python': (88.7, 0.1), 'JavaScript': (41.6, 0), 'Java': (38.4, 0),
                  'C#': (32.3, 0.1), 'TypeScript': (28.3, 0.1), 'PHP': (25.8, 0.1),
                  'C++': (20.5, 0), 'C': (18.2, 0.1), 'Go': (9.4, 0), 'SQL': (16.36, 0.1),
                  'Visual Basic': (4.36, 0), 'R': (7.96, 0), 'Swift': (18.43, 0.1)}


win = Tk()
pcc = PCC(win)

thread = threading.Timer(5.0, Test)
thread.start()

win.protocol('WM_DELETE_WINDOW', exit)
win.mainloop()
