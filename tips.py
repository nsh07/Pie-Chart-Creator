'''
Get a pop-up window when hovered to any widget with a short
message for what that widgets is designed for.
'''


import tkinter.tix as tix


class Tips:
    def __init__(self, window):
        self.balloon = tix.Balloon(window)

    def set_tips(self, widget, message):
        '''Generating pop-up window'''

        self.balloon.bind_widget(widget, balloonmsg=message)
