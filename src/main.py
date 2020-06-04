import pandas as pd
import os
from datetime import date
from os import path
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

DATA_DIR = '../data/'
DATA_PATH_CLIENT = DATA_DIR + 'client.pkl'
DATA_PATH_ECHO = DATA_DIR + 'echo.pkl'
DEFAULT_COLUMN_WIDTH = 70
CLINICIANS = ["JMcG", "EMcG"]
RDVMS = ["Falmouth Veterinary Medicine"]

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

class Form(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.loadData()

        f1 = Frame(self)
        f1.pack(fill = X)

        # Labels for each field
        LEFT_LABEL_WIDTH = 16
        RIGHT_LABEL_WIDTH = 18
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Case/Client #").grid(row = 0, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Client").grid(row = 1, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Species / Breed / Sex").grid(row = 2, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Birth / Death").grid(row = 3, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "LA / FU Date").grid(row = 4, column = 0)
        Label(f1, anchor = "w", width = LEFT_LABEL_WIDTH,
            text = "Clinician").grid(row = 5, column = 0)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "Client Last / First").grid(row = 0, column = 4)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "City / ZIP / State").grid(row = 1, column = 4)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "Hm / Wk / Alt Phones").grid(row = 2, column = 4)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "RDVM Last / First").grid(row = 3, column = 4)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "Practice").grid(row = 4, column = 4)
        Label(f1, anchor = "w", width = RIGHT_LABEL_WIDTH,
            text = "RDVM Ph1 / Ph2 / FAX").grid(row = 5, column = 4)

        # Left column fields
        self.caseNum = Text(f1, width = 12, height = 1)
        self.caseNum.grid(row = 0, column = 1, padx = 2)
        self.clientNum = Text(f1, width = 12, height = 1)
        self.clientNum.grid(row = 0, column = 2, padx = 2)
        self.patient = Text(f1, width = 12, height = 1)
        self.patient.grid(row = 1, column = 1, padx = 2)
        self.species = Text(f1, width = 12, height = 1)
        self.species.grid(row = 2, column = 1, padx = 2)
        self.breed = Text(f1, width = 12, height = 1)
        self.breed.grid(row = 2, column = 2, padx = 2)
        self.sex = Text(f1, width = 4, height = 1)
        self.sex.grid(row = 2, column = 3, padx = 2)
        self.birth = DateEntry(f1)
        self.birth.grid(row = 3, column = 1, padx = 2)
        self.death = DateEntry(f1)
        self.death.grid(row = 3, column = 2, padx = 2)
        self.la = DateEntry(f1)
        self.la.grid(row = 4, column = 1, padx = 2)
        self.fu = DateEntry(f1)
        self.fu.grid(row = 4, column = 2, padx = 2)
        self.clinicianText = StringVar()
        self.clinician = ttk.Combobox(f1, width = 12, text = self.clinicianText, values = CLINICIANS)
        self.clinician.grid(row = 5, column = 1, padx = 2)

        # Right column fields
        self.clientLast = Text(f1, width = 12, height = 1)
        self.clientLast.grid(row = 0, column = 5, sticky = "w")
        self.clientFirst = Text(f1, width = 12, height = 1)
        self.clientFirst.grid(row = 0, column = 5,
            sticky = "w", padx = (105, 0))
        self.city = Text(f1, width = 12, height = 1)
        self.city.grid(row = 1, column = 5, sticky = "w")
        self.zipCode = Text(f1, width = 12, height = 1)
        self.zipCode.grid(row = 1, column = 5, sticky = "w", padx = (105, 0))
        self.state = Text(f1, width = 4, height = 1)
        self.state.grid(row = 1, column = 5, sticky = "w", padx = (210, 0))
        self.homePhone = Text(f1, width = 12, height = 1)
        self.homePhone.grid(row = 2, column = 5, sticky = "w")
        self.workPhone = Text(f1, width = 12, height = 1)
        self.workPhone.grid(row = 2, column = 5, sticky = "w", padx = (105, 0))
        self.altPhone = Text(f1, width = 12, height = 1)
        self.altPhone.grid(row = 2, column = 5, sticky = "w", padx = (210, 0))
        self.rdvmLast = Text(f1, width = 12, height = 1)
        self.rdvmLast.grid(row = 3, column = 5, sticky = "w")
        self.rdvmFirst = Text(f1, width = 12, height = 1)
        self.rdvmFirst.grid(row = 3, column = 5, sticky = "w", padx = (105, 0))
        self.practiceText = StringVar()
        self.practice = ttk.Combobox(f1, width = 31, text = self.practiceText, values = RDVMS)
        self.practice.grid(row = 4, column = 5, sticky = "w")
        self.rdvmPhone1 = Text(f1, width = 12, height = 1)
        self.rdvmPhone1.grid(row = 5, column = 5, sticky = "w")
        self.rdvmPhone2 = Text(f1, width = 12, height = 1)
        self.rdvmPhone2.grid(row = 5, column = 5, sticky = "w", padx = (105, 0))
        self.rdvmFAX = Text(f1, width = 12, height = 1)
        self.rdvmFAX.grid(row = 5, column = 5, sticky = "w", padx = (210, 0))

        # Submit button
        self.submitButton = Button(f1, text = "Submit", fg = "Black",
            command = self.submit)
        self.submitButton.grid(row = 6, column = 5)

        # Frame 2 contains the information on pets
        #f2 = Frame(self, width = 100, expand = False)
        #f2.pack(pady = 10)

        # Fills with the form information.
        f2 = ScrollableFrame(self, height = 150)

        # Listbox all the basic pet information
        self.numEntries = len(self.data.values)
        self.listBox = ttk.Treeview(f2.scrollable_frame, height = self.numEntries, columns = list(self.data.columns), show = 'headings')
        i = 0
        for col in self.data.columns:
            self.listBox.heading(i, text = col)
            self.listBox.column(i, width = DEFAULT_COLUMN_WIDTH)
            i += 1
        i = 0
        for item in self.data.values:
            self.listBox.insert("", "end", text = str(i), values = list(item))
            i += 1

        # Get info on click
        self.listBox.bind("<Double-1>", self.fillFields)

        self.listBox.pack(fill = BOTH, expand = True)
        f2.pack(fill = BOTH, expand = True, pady = 10)

        self.tab = Echo(self)
        self.tab.pack(fill = X)


    def loadData(self):
        # Read data
        if path.exists(DATA_PATH_CLIENT):
            self.data = pd.read_pickle(DATA_PATH_CLIENT)
        else:
            # Or create data
            d = {'Case number': [],
                'Client number': [],
                'Patient': [],
                'Species': [],
                'Breed': [],
                'Sex': [],
                'Birthdate': [],
                'Deathdate': [],
                'LAdate': [],
                'FUdate': [],
                'Client last': [],
                'Client first': [],
                'Clinician': [],
                'City': [],
                'State': [],
                'ZIP': [],
                'Home phone': [],
                'Work phone': [],
                'Alt phone': [],
                'RDVM last': [],
                'RDVM first': [],
                'Practice': [],
                'RDVM phone 1': [],
                'RDVM phone 2': [],
                'RDVM fax': []}
            self.data = pd.DataFrame(d)

    def submit(self):
        newData = {
            'Case number': self.caseNum.get("1.0", "end-1c"),
            'Client number': self.clientNum.get("1.0", "end-1c"),
            'Patient': self.patient.get("1.0", "end-1c"),
            'Species': self.species.get("1.0", "end-1c"),
            'Breed': self.breed.get("1.0", "end-1c"),
            'Sex': self.sex.get("1.0", "end-1c"),
            'Birthdate': self.birth.get(),
            'Deathdate': self.death.get(),
            'LAdate': self.la.get(),
            'FUdate': self.fu.get(),
            'Client last': self.clientLast.get("1.0", "end-1c"),
            'Client first': self.clientFirst.get("1.0", "end-1c"),
            'Clinician': self.clinician.get(),
            'City': self.city.get("1.0", "end-1c"),
            'State': self.state.get("1.0", "end-1c"),
            'ZIP': self.zipCode.get("1.0", "end-1c"),
            'Home phone': self.homePhone.get("1.0", "end-1c"),
            'Work phone': self.workPhone.get("1.0", "end-1c"),
            'Alt phone': self.altPhone.get("1.0", "end-1c"),
            'RDVM last': self.rdvmLast.get("1.0", "end-1c"),
            'RDVM first': self.rdvmFirst.get("1.0", "end-1c"),
            'Practice': self.practice.get(),
            'RDVM phone 1': self.rdvmPhone1.get("1.0", "end-1c"),
            'RDVM phone 2': self.rdvmPhone2.get("1.0", "end-1c"),
            'RDVM fax': self.rdvmFAX.get("1.0", "end-1c")}

        self.listBox.insert("", "end", values = list(newData.values()))
        self.data = self.data.append(newData, ignore_index = True)
        self.clearFields()

        self.numEntries += 1
        self.listBox.configure(height = self.numEntries)

        self.saveData()

    def saveData(self):
        # Create the data folder if it doesn't exist
        if not path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        # Save data
        self.data.to_pickle(DATA_PATH_CLIENT)

    def clearFields(self):
        self.setText(self.caseNum, "")
        self.setText(self.clientNum, "")
        self.setText(self.patient, "")
        self.setText(self.species, "")
        self.setText(self.breed, "")
        self.setText(self.sex, "")
        self.birth.set_date(date.today())
        self.death.set_date(date.today())
        self.la.set_date(date.today())
        self.fu.set_date(date.today())
        self.setText(self.clientLast, "")
        self.setText(self.clientFirst, "")
        self.clinicianText.set("")
        self.setText(self.city, "")
        self.setText(self.state, "")
        self.setText(self.zipCode, "")
        self.setText(self.homePhone, "")
        self.setText(self.workPhone, "")
        self.setText(self.altPhone, "")
        self.setText(self.rdvmLast, "")
        self.setText(self.rdvmFirst, "")
        self.practiceText.set("")
        self.setText(self.rdvmPhone1, "")
        self.setText(self.rdvmPhone2, "")
        self.setText(self.rdvmFAX, "")

        self.submitButton.configure(text = "Submit", command = self.submit)

    def fillFields(self, event = None):
        if self.listBox.selection():
            item = self.listBox.selection()[0]
            values = self.listBox.item(item, "values")

            self.setText(self.caseNum, values[0])
            self.setText(self.clientNum, values[1])
            self.setText(self.patient, values[2])
            self.setText(self.species, values[3])
            self.setText(self.breed, values[4])
            self.setText(self.sex, values[5])
            self.birth.set_date(values[6])
            self.death.set_date(values[7])
            self.la.set_date(values[8])
            self.fu.set_date(values[9])
            self.setText(self.clientLast, values[10])
            self.setText(self.clientFirst, values[11])
            self.clinicianText.set(values[12])
            self.setText(self.city, values[13])
            self.setText(self.state, values[14])
            self.setText(self.zipCode, values[15])
            self.setText(self.homePhone, values[16])
            self.setText(self.workPhone, values[17])
            self.setText(self.altPhone, values[18])
            self.setText(self.rdvmLast, values[19])
            self.setText(self.rdvmFirst, values[20])
            self.practiceText.set(values[21])
            self.setText(self.rdvmPhone1, values[22])
            self.setText(self.rdvmPhone2, values[23])
            self.setText(self.rdvmFAX, values[24])

            self.submitButton.configure(text = "Modify", command = lambda: self.modify(item))

    def modify(self, item):
        moddedData = {
            'Case number': self.caseNum.get("1.0", "end-1c"),
            'Client number': self.clientNum.get("1.0", "end-1c"),
            'Patient': self.patient.get("1.0", "end-1c"),
            'Species': self.species.get("1.0", "end-1c"),
            'Breed': self.breed.get("1.0", "end-1c"),
            'Sex': self.sex.get("1.0", "end-1c"),
            'Birthdate': self.birth.get(),
            'Deathdate': self.death.get(),
            'LAdate': self.la.get(),
            'FUdate': self.fu.get(),
            'Client last': self.clientLast.get("1.0", "end-1c"),
            'Client first': self.clientFirst.get("1.0", "end-1c"),
            'Clinician': self.clinician.get(),
            'City': self.city.get("1.0", "end-1c"),
            'State': self.state.get("1.0", "end-1c"),
            'ZIP': self.zipCode.get("1.0", "end-1c"),
            'Home phone': self.homePhone.get("1.0", "end-1c"),
            'Work phone': self.workPhone.get("1.0", "end-1c"),
            'Alt phone': self.altPhone.get("1.0", "end-1c"),
            'RDVM last': self.rdvmLast.get("1.0", "end-1c"),
            'RDVM first': self.rdvmFirst.get("1.0", "end-1c"),
            'Practice': self.practice.get(),
            'RDVM phone 1': self.rdvmPhone1.get("1.0", "end-1c"),
            'RDVM phone 2': self.rdvmPhone2.get("1.0", "end-1c"),
            'RDVM fax': self.rdvmFAX.get("1.0", "end-1c")}
        self.listBox.item(item, values = list(moddedData.values()))

        row = int(item[-1]) - 1

        self.data.loc[row] = list(moddedData.values())
        self.clearFields()

        self.saveData()

    def setText(self, widget, value):
        widget.delete(1.0, "end-1c")
        widget.insert("end-1c", value)

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

class Echo(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

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
        self.numEntries = len(self.data.values)
        self.listBox = ttk.Treeview(f2.scrollable_frame, height = self.numEntries, columns = list(self.data.columns), show = 'headings')
        i = 0
        for col in self.data.columns:
            self.listBox.heading(i, text = col)
            self.listBox.column(i, width = DEFAULT_COLUMN_WIDTH)
            i += 1
        i = 0
        for item in self.data.values:
            self.listBox.insert("", "end", text = str(i), values = list(item))
            i += 1

        # Get info on click
        self.listBox.bind("<Double-1>", self.fillFields)

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

    def saveData(self):
        # Create the data folder if it doesn't exist
        if not path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        # Save data
        self.data.to_pickle(DATA_PATH_ECHO)

    def loadData(self):
        # Read data
        if path.exists(DATA_PATH_ECHO):
            self.data = pd.read_pickle(DATA_PATH_ECHO)
        else:
            # Or create data
            d = {'Date': [],
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

    def fillFields(self, event = None):
        if self.listBox.selection():
            item = self.listBox.selection()[0]
            values = self.listBox.item(item, "values")

            self.date.set_date(values[0])
            self.setText(self.tape, values[1])
            self.setText(self.lbs, values[2])
            self.setText(self.kgs, "") #TODO: Where are some of these fields stored?
            self.setText(self.bsa, "")
            self.setText(self.hr, values[3])
            self.setText(self.rr, values[4])
            self.setText(self.ao, values[13])
            self.setText(self.la, values[14])
            self.setText(self.la2, "")
            self.setText(self.la2d, "")
            self.setText(self.epss, values[16])
            self.calcgroup.set("")
            self.setText(self.rv, values[9])
            self.setText(self.rv2, values[5])
            self.setText(self.ivs, values[10])
            self.setText(self.ivs2, values[6])
            self.setText(self.lvid, values[11])
            self.setText(self.lvid2, values[7])
            self.setText(self.lvw, values[12])
            self.setText(self.lvw2, values[8])
            self.vidxtext.set("")
            self.vidxtext2.set("")
            self.updateDeltas()

            self.delete.configure(state = "normal", command = lambda: self.deleteDataItem(item))

    def modify(self, item):
        moddedData = {
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

        self.saveData()

    def clearFields(self):
        self.date.set_date(date.today())
        self.setText(self.tape, "")
        self.setText(self.lbs, "")
        self.setText(self.kgs, "")
        self.setText(self.bsa, "")
        self.setText(self.hr, "")
        self.setText(self.rr, "")
        self.setText(self.ao, "")
        self.setText(self.la, "")
        self.setText(self.la2, "")
        self.setText(self.la2d, "")
        self.setText(self.epss, "")
        self.calcgroup.set("")
        self.setText(self.rv, "")
        self.setText(self.rv2, "")
        self.setText(self.ivs, "")
        self.setText(self.ivs2, "")
        self.delt1.set("")
        self.setText(self.lvid, "")
        self.setText(self.lvid2, "")
        self.delt2.set("")
        self.setText(self.lvw, "")
        self.setText(self.lvw2, "")
        self.delt3.set("")
        self.vidxtext.set("")
        self.vidxtext2.set("")
        self.delt4.set("")

        self.delete.configure(state = "disabled", command = None)

    def deleteDataItem(self, item):
        # TODO make this work
        row = int(item[-1]) - 1
        self.listBox.delete(item)

        self.numEntries -= 1
        self.listBox.configure(height = self.numEntries)

        self.data = self.data.drop(self.data.index[row])
        self.saveData()
        self.clearFields()

    def indices(self):
        # TODO this is acting like a submit, when it really does something else
        print("Indices")


        newData = {
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

        self.saveData()

    def setText(self, widget, value):
        widget.delete(1.0, "end-1c")
        widget.insert("end-1c", value)


# Create a GUI window
root = Tk()

root.title("Veterinary Software")
root.geometry("860x700")

# Fills with the form information.
f1 = ScrollableFrame(root)
f2 = Form(f1.scrollable_frame).pack(padx = 15, pady = 15, fill = BOTH, expand = True)
f1.pack(fill = BOTH, expand = True)

# Start the GUI
root.mainloop()