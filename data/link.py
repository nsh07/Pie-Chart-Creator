'''
Open the github repository to view the codes of this program
'''

import requests
import webbrowser
from tkinter import messagebox


def is_internet():
    '''Check if you are connected to internet'''

    try:
        requests.get('http://google.com')
        return True

    except requests.ConnectionError:
        return False


def open_link(master, event=None):
    '''Open the github page of the author(NMrocks) in the default browser'''

    if is_internet():
        master.after(0, lambda: webbrowser.open('http://github.com/NMrocks/Pie-Chart-Creator'))

    else:
        messagebox.showerror('ERROR', 'Unable to load page because you are not connected to internet')
