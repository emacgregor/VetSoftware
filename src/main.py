from tkinter import *
from Form import Form
from util import *

# Create a GUI window
root = Tk()

root.title("Veterinary Software")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))

# Fills with the form information.
f1 = ScrollableFrame(root)
f2 = Form(f1.scrollable_frame).pack(padx = PADDING, pady = PADDING, fill = BOTH, expand = True)
f1.pack(fill = BOTH, expand = True)

# Start the GUI
root.mainloop()