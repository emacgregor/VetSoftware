from tkinter import *
from tkinter import ttk
from datetime import date
from os import path
from util import *
from tkcalendar import DateEntry
import pandas as pd

class Echo(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.client = self.parent.client
        self.clientTextVar = StringVar()
        self.clientTextVar.set(self.client)

        self.loadData()

        f1 = Frame(self)
        f1.pack(fill = X)

        # Labels for each field
        LABEL_WIDTH1 = 6
        LABEL_WIDTH2 = 5
        LABEL_WIDTH3 = 5
        LABEL_WIDTH4 = 16
        LABEL_WIDTH5 = 5
        LABEL_WIDTH6 = 8
        LABEL_WIDTH7 = 8
        LABEL_WIDTH8 = 10

        Label(f1, anchor = "w", width = LABEL_WIDTH1,
            text = "Client").grid(row = 0, column = 0)
        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            textvariable = self.clientTextVar).grid(row = 0, column = 1)

        Label(f1, anchor = "w", width = LABEL_WIDTH1,
            text = "Date").grid(row = 1, column = 0)
        Label(f1, anchor = "w", width = LABEL_WIDTH1,
            text = "Tape").grid(row = 2, column = 0)

        self.date = DateEntry(f1)
        self.date.grid(row = 1, column = 1, padx = 2)
        self.tape = Text(f1, width = 12, height = 1)
        self.tape.grid(row = 2, column = 1, padx = 2)

        # Delete button
        self.delete = Button(f1, text = "Delete", fg = "Black", state = "disabled")
        self.delete.grid(row = 4, column = 1)

        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            text = "LBS").grid(row = 1, column = 2)
        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            text = "KGS").grid(row = 2, column = 2)
        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            text = "BSA").grid(row = 3, column = 2)
        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            text = "HR").grid(row = 4, column = 2)
        Label(f1, anchor = "w", width = LABEL_WIDTH2,
            text = "RR").grid(row = 5, column = 2)

        self.lbs = Text(f1, width = 4, height = 1)
        self.lbs.grid(row = 1, column = 3, padx = 2)
        self.kgs = Text(f1, width = 4, height = 1)
        self.kgs.grid(row = 2, column = 3, padx = 2)
        self.bsa = Text(f1, width = 4, height = 1)
        self.bsa.grid(row = 3, column = 3, padx = 2)
        self.hr = Text(f1, width = 4, height = 1)
        self.hr.grid(row = 4, column = 3, padx = 2)
        self.rr = Text(f1, width = 4, height = 1)
        self.rr.grid(row = 5, column = 3, padx = 2)

        Label(f1, anchor = "w", width = LABEL_WIDTH3,
            text = "Ao").grid(row = 1, column = 4)
        Label(f1, anchor = "w", width = LABEL_WIDTH3,
            text = "LA").grid(row = 2, column = 4)
        Label(f1, anchor = "w", width = LABEL_WIDTH3,
            text = "LA2").grid(row = 3, column = 4)
        Label(f1, anchor = "w", width = LABEL_WIDTH3,
            text = "LA2D").grid(row = 4, column = 4)
        Label(f1, anchor = "w", width = LABEL_WIDTH3,
            text = "EPSS").grid(row = 5, column = 4)

        self.ao = Text(f1, width = 4, height = 1)
        self.ao.grid(row = 1, column = 5, padx = 2)
        self.la = Text(f1, width = 4, height = 1)
        self.la.grid(row = 2, column = 5, padx = 2)
        self.la2 = Text(f1, width = 4, height = 1)
        self.la2.grid(row = 3, column = 5, padx = 2)
        self.la2d = Text(f1, width = 4, height = 1)
        self.la2d.grid(row = 4, column = 5, padx = 2)
        self.epss = Text(f1, width = 4, height = 1)
        self.epss.grid(row = 5, column = 5, padx = 2)

        Label(f1, anchor = "w", width = LABEL_WIDTH4,
            text = "Calculation Group").grid(row = 1, column = 6)
        self.calcgroup = ttk.Combobox(f1, width = LABEL_WIDTH4,
            values = CLINICIANS)
        self.calcgroup.grid(row = 2, column = 6, padx = 20)

        Label(f1, anchor = "w", width = LABEL_WIDTH5,
            text = "RV").grid(row = 1, column = 7)
        Label(f1, anchor = "w", width = LABEL_WIDTH5,
            text = "IVS").grid(row = 2, column = 7)
        Label(f1, anchor = "w", width = LABEL_WIDTH5,
            text = "LVID").grid(row = 3, column = 7)
        Label(f1, anchor = "w", width = LABEL_WIDTH5,
            text = "LVW").grid(row = 4, column = 7)
        Label(f1, anchor = "w", width = LABEL_WIDTH5,
            text = "VIDX").grid(row = 5, column = 7)

        Label(f1, width = LABEL_WIDTH6,
            text = "Systole").grid(row = 0, column = 8)

        self.rv = CustomText(f1, width = LABEL_WIDTH6, height = 1)
        self.rv.grid(row = 1, column = 8, padx = 2)
        self.ivs = CustomText(f1, width = LABEL_WIDTH6, height = 1)
        self.ivs.grid(row = 2, column = 8, padx = 2)
        self.lvid = CustomText(f1, width = LABEL_WIDTH6, height = 1)
        self.lvid.grid(row = 3, column = 8, padx = 2)
        self.lvw = CustomText(f1, width = LABEL_WIDTH6, height = 1)
        self.lvw.grid(row = 4, column = 8, padx = 2)
        self.vidxtext = StringVar()
        self.vidx = Entry(f1, textvariable = self.vidxtext, width = LABEL_WIDTH8, state = 'readonly')
        self.vidx.grid(row = 5, column = 8, padx = 2)

        Label(f1, width = LABEL_WIDTH7,
            text = "Diastole").grid(row = 0, column = 9)

        self.rv2 = CustomText(f1, width = LABEL_WIDTH7, height = 1)
        self.rv2.grid(row = 1, column = 9, padx = 2)
        self.ivs2 = CustomText(f1, width = LABEL_WIDTH7, height = 1)
        self.ivs2.grid(row = 2, column = 9, padx = 2)
        self.lvid2 = CustomText(f1, width = LABEL_WIDTH7, height = 1)
        self.lvid2.grid(row = 3, column = 9, padx = 2)
        self.lvw2 = CustomText(f1, width = LABEL_WIDTH7, height = 1)
        self.lvw2.grid(row = 4, column = 9, padx = 2)
        self.vidxtext2 = StringVar()
        self.vidx2 = Entry(f1, textvariable = self.vidxtext2, width = LABEL_WIDTH8, state = 'readonly')
        self.vidx2.grid(row = 5, column = 9, padx = 2)

        self.rv.bind("<<TextModified>>", self.updateDeltas)
        self.rv2.bind("<<TextModified>>", self.updateDeltas)
        self.ivs.bind("<<TextModified>>", self.updateDeltas)
        self.ivs2.bind("<<TextModified>>", self.updateDeltas)
        self.lvid.bind("<<TextModified>>", self.updateDeltas)
        self.lvid2.bind("<<TextModified>>", self.updateDeltas)
        self.lvw.bind("<<TextModified>>", self.updateDeltas)
        self.lvw2.bind("<<TextModified>>", self.updateDeltas)

        Label(f1, width = LABEL_WIDTH8, text = "Δ").grid(row = 0, column = 10)

        self.delt1 = StringVar()
        self.delt2 = StringVar()
        self.delt3 = StringVar()
        self.delt4 = StringVar()
        self.ivs3 = Entry(f1, textvariable = self.delt1, width = LABEL_WIDTH8, state = 'readonly')
        self.ivs3.grid(row = 2, column = 10, padx = 2)
        self.lvid3 = Entry(f1, textvariable = self.delt2, width = LABEL_WIDTH8, state = 'readonly')
        self.lvid3.grid(row = 3, column = 10, padx = 2)
        self.lvw3 = Entry(f1, textvariable = self.delt3, width = LABEL_WIDTH8, state = 'readonly')
        self.lvw3.grid(row = 4, column = 10, padx = 2)
        self.vidx3 = Entry(f1, textvariable = self.delt4, width = LABEL_WIDTH8, state = 'readonly')
        self.vidx3.grid(row = 5, column = 10, padx = 2)

        self.indices = Button(f1, text = "Indices", fg = "Black",
            command = self.indices)
        self.indices.grid(row = 2, column = 11)

        # Fills with the form information.
        f2 = ScrollableFrame(self, height = 150)

        # Listbox all the basic pet information
        self.numEntries = 0
        self.listBox = ttk.Treeview(f2.scrollable_frame, columns = list(self.data.columns), show = 'headings')

        i = 0
        for col in self.data.columns[1:]:
            self.listBox.heading(i, text = col)
            self.listBox.column(i, width = columnWidth(len(self.data.columns)))
            i += 1
        for item in self.data.values:
            if (item[0] == self.client):
                self.listBox.insert("", "end", values = list(item)[1:])
                self.numEntries += 1
        self.listBox.configure(height = self.numEntries)

        # Get info on click
        self.listBox.bind("<Double-1>", self.onSelection)

        self.listBox.pack(fill = BOTH, expand = True)
        f2.pack(fill = BOTH, expand = True, pady = 10)

    def updateDeltas(self, event = None):
        #TODO: Find out how these delts work
        try:
            self.delt1.set(float(self.ivs.get("1.0", "end-1c"))
                - float(self.ivs2.get("1.0", "end-1c")))
        except ValueError:
            self.delt1.set("")
        try:
            self.delt2.set(float(self.lvid.get("1.0", "end-1c"))
                - float(self.lvid2.get("1.0", "end-1c")))
        except ValueError:
            self.delt2.set("")
        try:
            self.delt3.set(float(self.lvw.get("1.0", "end-1c"))
                - float(self.lvw2.get("1.0", "end-1c")))
        except ValueError:
            self.delt3.set("")

    def loadData(self):
        # Read data
        if path.exists(DATA_PATH_ECHO):
            self.data = pd.read_pickle(DATA_PATH_ECHO)
        else:
            self.initializeData()

    def initializeData(self):
        d = {
            'ClientNum': [],
            'Date': [],
            'Tape': [],
            'LBS': [],
            'HR': [],
            'RR': [],
            'RVd': [],
            'IVSd': [],
            'LVIDd': [],
            'LVWd': [],
            'RVs': [],
            'IVSs': [],
            'LVIDs': [],
            'LVWs': [],
            'Ao': [],
            'LA': [],
            'LAm': [],
            'EPSS': [],
            'SAxLA D': [],
            'SAx Ao D': [],
            'SAx LA A': [],
            'LAx LA D': [],
            'Dep': [],
            'Len': [],
            'Gir': [],
            'Wld': []}
        self.data = pd.DataFrame(d)

    def onSelection(self, event = None):
        if self.listBox.selection():
            item = self.listBox.selection()[0]
            values = self.listBox.item(item, "values")
            self.fillFields(values)
            self.delete.configure(state = "normal", command = lambda: self.deleteDataItem(item))

    def fillFields(self, values):
            self.date.set_date(values[0])
            setText(self.tape, values[1])
            setText(self.lbs, values[2])
            setText(self.kgs, "") #TODO: Where are some of these fields stored?
            setText(self.bsa, "")
            setText(self.hr, values[3])
            setText(self.rr, values[4])
            setText(self.ao, values[13])
            setText(self.la, values[14])
            setText(self.la2, "")
            setText(self.la2d, "")
            setText(self.epss, values[16])
            self.calcgroup.set("")
            setText(self.rv, values[9])
            setText(self.rv2, values[5])
            setText(self.ivs, values[10])
            setText(self.ivs2, values[6])
            setText(self.lvid, values[11])
            setText(self.lvid2, values[7])
            setText(self.lvw, values[12])
            setText(self.lvw2, values[8])
            self.vidxtext.set("")
            self.vidxtext2.set("")
            self.updateDeltas()

    def modify(self, item):
        moddedData = {
            'ClientNum': self.client,
            'Date': self.date.get(),
            'Tape': self.tape.get("1.0", "end-1c"),
            'LBS': self.lbs.get("1.0", "end-1c"),
            'HR': self.hr.get("1.0", "end-1c"),
            'RR': self.rr.get("1.0", "end-1c"),
            'RVd': self.rv2.get("1.0", "end-1c"),
            'IVSd': self.ivs2.get("1.0", "end-1c"),
            'LVIDd': self.lvid2.get("1.0", "end-1c"),
            'LVWd': self.lvw2.get("1.0", "end-1c"),
            'RVs': self.rv.get("1.0", "end-1c"),
            'IVSs': self.ivs.get("1.0", "end-1c"),
            'LVIDs': self.lvid.get("1.0", "end-1c"),
            'LVWs': self.lvw.get("1.0", "end-1c"),
            'Ao': self.ao.get("1.0", "end-1c"),
            'LA': self.la.get("1.0", "end-1c"),
            'LAm': "", # TODO: What are these fields?
            'EPSS': "",
            'SAxLA D': "",
            'SAx Ao D': "",
            'SAx LA A': "",
            'LAx LA D': "",
            'Dep': "",
            'Len': "",
            'Gir': "",
            'Wld': ""}
        self.listBox.item(item, values = list(moddedData.values()))

        row = int(item[-1]) - 1

        self.data.loc[row] = list(moddedData.values())
        self.clearFields()

        saveData(self.data, DATA_PATH_ECHO)

    def clearFields(self):
        self.date.set_date(date.today())
        setText(self.tape, "")
        setText(self.lbs, "")
        setText(self.kgs, "")
        setText(self.bsa, "")
        setText(self.hr, "")
        setText(self.rr, "")
        setText(self.ao, "")
        setText(self.la, "")
        setText(self.la2, "")
        setText(self.la2d, "")
        setText(self.epss, "")
        self.calcgroup.set("")
        setText(self.rv, "")
        setText(self.rv2, "")
        setText(self.ivs, "")
        setText(self.ivs2, "")
        self.delt1.set("")
        setText(self.lvid, "")
        setText(self.lvid2, "")
        self.delt2.set("")
        setText(self.lvw, "")
        setText(self.lvw2, "")
        self.delt3.set("")
        self.vidxtext.set("")
        self.vidxtext2.set("")
        self.delt4.set("")

        self.delete.configure(state = "disabled", command = None)

    def deleteDataItem(self, item):
        row = int(item[-1]) - 1
        self.listBox.delete(item)

        self.numEntries -= 1
        self.listBox.configure(height = self.numEntries)

        self.data = self.data.drop(self.data.index[row])
        saveData(self.data, DATA_PATH_ECHO)
        self.clearFields()

    def indices(self):
        # TODO this is acting like a submit, when it really does something else
        print("Indices")


        newData = {
            'ClientNum': self.client,
            'Date': self.date.get(),
            'Tape': self.tape.get("1.0", "end-1c"),
            'LBS': self.lbs.get("1.0", "end-1c"),
            'HR': self.hr.get("1.0", "end-1c"),
            'RR': self.rr.get("1.0", "end-1c"),
            'RVd': self.rv2.get("1.0", "end-1c"),
            'IVSd': self.ivs2.get("1.0", "end-1c"),
            'LVIDd': self.lvid2.get("1.0", "end-1c"),
            'LVWd': self.lvw2.get("1.0", "end-1c"),
            'RVs': self.rv.get("1.0", "end-1c"),
            'IVSs': self.ivs.get("1.0", "end-1c"),
            'LVIDs': self.lvid.get("1.0", "end-1c"),
            'LVWs': self.lvw.get("1.0", "end-1c"),
            'Ao': self.ao.get("1.0", "end-1c"),
            'LA': self.la.get("1.0", "end-1c"),
            'LAm': "", # TODO: What are these fields?
            'EPSS': "",
            'SAxLA D': "",
            'SAx Ao D': "",
            'SAx LA A': "",
            'LAx LA D': "",
            'Dep': "",
            'Len': "",
            'Gir': "",
            'Wld': ""}

        self.listBox.insert("", "end", values = list(newData.values()))
        self.data = self.data.append(newData, ignore_index = True)
        self.clearFields()

        self.numEntries += 1
        self.listBox.configure(height = self.numEntries)

        saveData(self.data, DATA_PATH_ECHO)

    def updateClient(self, client):
        self.client = client[1]
        self.clientTextVar.set(client[2])
        self.listBox.delete(*self.listBox.get_children())
        self.numEntries = 0
        for item in self.data.values:
            if (item[0] == self.client):
                self.listBox.insert("", "end", values = list(item)[1:])
                self.numEntries += 1
        self.listBox.configure(height = self.numEntries)

    def modifiedClient(self, client):
        # We need to update the corresponding client number here when it's updated in Client
        for item in self.data.values:
            if (item[0] == self.client):
                item[0] = client[1]
        self.updateClient(client)
        saveData(self.data, DATA_PATH_ECHO)