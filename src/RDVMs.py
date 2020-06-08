from tkinter import *
from tkinter import ttk
from util import *
import pandas as pd
from os import path

class RDVMs(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.loadData()

        f1 = Frame(self)
        f1.pack(fill = X)

        # Labels for each field
        LEFT_LABEL_WIDTH = 14
        RIGHT_LABEL_WIDTH = 8
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Practice").grid(row = 0, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Address").grid(row = 1, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "City / State / Zip").grid(row = 2, column = 0)

        self.practice = Text(f1, width = 26, height = 1)
        self.practice.grid(row = 0, column = 1, sticky = "w")
        self.address = Text(f1, width = 26, height = 1)
        self.address.grid(row = 1, column = 1, sticky = "w")
        self.city = Text(f1, width = 12, height = 1)
        self.city.grid(row = 2, column = 1, sticky = "w")
        self.state = Text(f1, width = 4, height = 1)
        self.state.grid(row = 2, column = 1, sticky = "w", padx = (104, 0))
        self.zipCode = Text(f1, width = 8, height = 1)
        self.zipCode.grid(row = 2, column = 1, sticky = "w", padx = (144, 0))

        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "Phone 1").grid(row = 0, column = 2)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "Phone 2").grid(row = 1, column = 2)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "FAX").grid(row = 2, column = 2)

        self.ph1 = Text(f1, width = 20, height = 1)
        self.ph1.grid(row = 0, column = 3, sticky = "w")
        self.ph2 = Text(f1, width = 20, height = 1)
        self.ph2.grid(row = 1, column = 3, sticky = "w")
        self.fax = Text(f1, width = 20, height = 1)
        self.fax.grid(row = 2, column = 3, sticky = "w")

        self.submitButton = Button(f1, text = "Submit", fg = "Black",
            command = self.submit)
        self.submitButton.grid(row = 0, column = 5)
        self.deleteButton = Button(f1, text = "Delete", fg = "Black",
            state = "disabled")
        self.deleteButton.grid(row = 0, column = 6)
        self.clearButton = Button(f1, text = "New", fg = "Black",
            command = self.clearFields)
        self.clearButton.grid(row = 0, column = 7)

        # Fills with the form information.
        self.f2 = ScrollableFrame(self, height = 150)

        self.listBox = None
        self.buildTable()

        self.f2.pack(fill = BOTH, expand = True, pady = 10)

    def loadData(self):
        # Read data
        if path.exists(DATA_PATH_RDVMS):
            self.data = pd.read_pickle(DATA_PATH_RDVMS)
        else:
            self.initializeData()

    def initializeData(self):
        d = {'Practice': [],
            'Address': [],
            'City': [],
            'ST': [],
            'Zip': [],
            'Ph1': [],
            'Ph2': [],
            'FAX': []}
        self.data = pd.DataFrame(d)

    def fillFields(self, values):
        setText(self.practice, values[0])
        setText(self.address, values[1])
        setText(self.city, values[2])
        setText(self.state, values[3])
        setText(self.zipCode, values[4])
        setText(self.ph1, values[5])
        setText(self.ph2, values[6])
        setText(self.fax, values[7])

    def onSelection(self, event = None):
        if self.listBox.selection():
            item = self.listBox.selection()[0]
            values = self.listBox.item(item, "values")
            self.fillFields(values)
            self.submitButton.configure(text = "Modify", command = lambda: self.modify(item))
            self.deleteButton.configure(state = "active", command = lambda: self.deleteDataItem(item))

    def clearFields(self):
        setText(self.practice, "")
        setText(self.address, "")
        setText(self.city, "")
        setText(self.state, "")
        setText(self.zipCode, "")
        setText(self.ph1, "")
        setText(self.ph2, "")
        setText(self.fax, "")
        self.submitButton.configure(text = "Submit", command = self.submit)
        self.deleteButton.configure(state = "disabled")

    def buildTable(self):
        # Listbox contains all the basic pet information
        self.numEntries = len(self.data.values)

        if self.listBox is not None:
            self.listBox.pack_forget()
        self.listBox = ttk.Treeview(self.f2.scrollable_frame, height = self.numEntries, columns = list(self.data.columns), show = 'headings')
        i = 0
        for col in self.data.columns:
            self.listBox.heading(i, text = col)
            self.listBox.column(i, width = columnWidth(len(self.data.columns)))
            i += 1
        for item in self.data.values:
            self.listBox.insert("", "end", values = list(item))

        # Get info on click
        self.listBox.bind("<Double-1>", self.onSelection)

        self.listBox.pack(fill = BOTH, expand = True)

    def submit(self, event = None):
        newData = {'Practice': self.practice.get("1.0", "end-1c"),
            'Address': self.address.get("1.0", "end-1c"),
            'City': self.city.get("1.0", "end-1c"),
            'ST': self.state.get("1.0", "end-1c"),
            'Zip': self.zipCode.get("1.0", "end-1c"),
            'Ph1': self.ph1.get("1.0", "end-1c"),
            'Ph2': self.ph2.get("1.0", "end-1c"),
            'FAX': self.fax.get("1.0", "end-1c")}

        self.data = self.data.append(newData, ignore_index = True)
        self.data = self.data.drop_duplicates(subset = "Practice", keep = 'last')
        self.buildTable()

        self.clearFields()
        self.saveAndUpdate()

    def modify(self, item):
        moddedData = {'Practice': self.practice.get("1.0", "end-1c"),
            'Address': self.address.get("1.0", "end-1c"),
            'City': self.city.get("1.0", "end-1c"),
            'ST': self.state.get("1.0", "end-1c"),
            'Zip': self.zipCode.get("1.0", "end-1c"),
            'Ph1': self.ph1.get("1.0", "end-1c"),
            'Ph2': self.ph2.get("1.0", "end-1c"),
            'FAX': self.fax.get("1.0", "end-1c")}
        self.listBox.item(item, values = list(moddedData.values()))

        row = int(item[-1]) - 1

        self.data.loc[row] = list(moddedData.values())

        self.clearFields()
        self.saveAndUpdate()

    def deleteDataItem(self, item):
        row = self.listBox.index(item)
        print(row)
        self.listBox.delete(item)

        self.numEntries -= 1
        self.listBox.configure(height = self.numEntries)

        self.data = self.data.drop(self.data.index[row])

        self.clearFields()
        self.saveAndUpdate()

    def updateParent(self):
        self.parent.updateRDVMs()

    def saveAndUpdate(self):
        saveData(self.data, DATA_PATH_RDVMS)
        self.updateParent()