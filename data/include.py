'''
The global function used by both main window and view window
'''


import os
import sys


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


def initial_position(window, title):
    '''Set window to the center of the screen at the startup'''

    window.withdraw()
    window.update()

    width, height = window.winfo_width(), window.winfo_height()
    screen_width, screen_height = window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2

    window.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

    window.resizable(0, 0)
    window.iconbitmap(resource_path('..\\pics\\icon.ico'))
    window.title(title)

    window.deiconify()
