import os
import math
from tkinter import *
from tkinter import ttk

DATA_DIR = '../data/'
DATA_PATH_CLIENT = DATA_DIR + 'client.pkl'
DATA_PATH_ECHO = DATA_DIR + 'echo.pkl'
DATA_PATH_RDVMS = DATA_DIR + 'rdvms.pkl'
DEFAULT_COLUMN_WIDTH = 70
CLINICIANS = ["JMcG", "EMcG"]
WIDTH = 860
HEIGHT = 700
PADDING = 15

def setText(widget, value):
    widget.delete(1.0, "end-1c")
    widget.insert("end-1c", value)

def saveData(data, path):
    # Create the data folder if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    # Save data
    data.to_pickle(path)

def columnWidth(numColumns):
	# 46 is for the width of the scrollbar
	return max(DEFAULT_COLUMN_WIDTH, math.floor((WIDTH - PADDING * 2 - 46) / numColumns))

# Thanks to Bryan Oakley on Stack Overflow https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
class CustomText(Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, height = 0, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, height = height, highlightthickness = 0)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )
        scrollbar = ttk.Scrollbar(self, orient = "horizontal", command = self.canvas.xview)
        scrollbar2 = ttk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.canvas.grid(row = 0, column = 0, sticky = NSEW)
        scrollbar.grid(row = 1, column = 0, sticky = EW)
        scrollbar2.grid(row = 0, column = 1, sticky = NS)
        self.canvas.configure(xscrollcommand = scrollbar.set, yscrollcommand = scrollbar2.set)

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")