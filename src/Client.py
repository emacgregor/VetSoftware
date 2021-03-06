import pandas as pd
from datetime import date
from os import path
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from Echo import Echo
from util import *

class Client(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.loadData()
        self.loadRDVMs()

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
        self.practice = ttk.Combobox(f1, width = 31, text = self.practiceText, values = list(self.rdvms.iloc[:,0]))
        self.practice.grid(row = 4, column = 5, sticky = "w")
        self.practice.bind("<<ComboboxSelected>>", self.onPracticeSelection)
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

        self.clearButton = Button(f1, text = "New", fg = "Black",
            command = self.clearFields)
        self.clearButton.grid(row = 6, column = 4)

        self.deleteButton = Button(f1, text = "Delete", fg = "Black",
            state = "disabled")
        self.deleteButton.grid(row = 6, column = 3)

        # Frame 2 contains the information on pets

        # Fills with the form information.
        f2 = ScrollableFrame(self, height = 150)

        # Listbox contains all the basic pet information
        self.numEntries = len(self.data.values)
        self.listBox = ttk.Treeview(f2.scrollable_frame, height = max(self.numEntries, 6), columns = list(self.data.columns), show = 'headings')
        i = 0
        for col in self.data.columns:
            self.listBox.heading(i, text = col)
            self.listBox.column(i, width = columnWidth(len(self.data.columns)))
            i += 1
        for item in self.data.values:
            self.listBox.insert("", "end", values = list(item))

        # Get info on click
        self.listBox.bind("<Double-1>", self.onTableSelection)

        self.listBox.pack(fill = BOTH, expand = True)

        f2.pack(fill = BOTH, expand = True, pady = 10)


    def loadData(self):
        # Read data
        if path.exists(DATA_PATH_CLIENT):
            self.data = pd.read_pickle(DATA_PATH_CLIENT)
        else:
            self.initializeData()

    def initializeData(self):
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
        self.listBox.configure(height = max(self.numEntries, 6))

        self.saveData()

    def clearFields(self):
        setText(self.caseNum, "")
        setText(self.clientNum, "")
        setText(self.patient, "")
        setText(self.species, "")
        setText(self.breed, "")
        setText(self.sex, "")
        self.birth.set_date(date.today())
        self.death.set_date(date.today())
        self.la.set_date(date.today())
        self.fu.set_date(date.today())
        setText(self.clientLast, "")
        setText(self.clientFirst, "")
        self.clinicianText.set("")
        setText(self.city, "")
        setText(self.state, "")
        setText(self.zipCode, "")
        setText(self.homePhone, "")
        setText(self.workPhone, "")
        setText(self.altPhone, "")
        setText(self.rdvmLast, "")
        setText(self.rdvmFirst, "")
        self.practiceText.set("")
        setText(self.rdvmPhone1, "")
        setText(self.rdvmPhone2, "")
        setText(self.rdvmFAX, "")

        self.parent.updateClient([])
        self.submitButton.configure(text = "Submit", command = self.submit)
        self.deleteButton.configure(state = "disabled")

    def onTableSelection(self, event = None):
        if self.listBox.selection():
            item = self.listBox.selection()[0]
            values = self.listBox.item(item, "values")
            self.fillFields(values)
            self.submitButton.configure(text = "Modify", command = lambda: self.modify(item))
            self.deleteButton.configure(state = "normal", command = lambda: self.deleteDataItem(item))
            self.parent.updateClient(values)

    def fillFields(self, values):
        setText(self.caseNum, values[0])
        setText(self.clientNum, values[1])
        setText(self.patient, values[2])
        setText(self.species, values[3])
        setText(self.breed, values[4])
        setText(self.sex, values[5])
        self.birth.set_date(values[6])
        self.death.set_date(values[7])
        self.la.set_date(values[8])
        self.fu.set_date(values[9])
        setText(self.clientLast, values[10])
        setText(self.clientFirst, values[11])
        self.clinicianText.set(values[12])
        setText(self.city, values[13])
        setText(self.state, values[14])
        setText(self.zipCode, values[15])
        setText(self.homePhone, values[16])
        setText(self.workPhone, values[17])
        setText(self.altPhone, values[18])
        setText(self.rdvmLast, values[19])
        setText(self.rdvmFirst, values[20])
        self.practiceText.set(values[21])
        setText(self.rdvmPhone1, values[22])
        setText(self.rdvmPhone2, values[23])
        setText(self.rdvmFAX, values[24])

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
        self.parent.modifiedData(list(moddedData.values()))

        self.saveData()

    def loadRDVMs(self):
        # Read data
        if path.exists(DATA_PATH_RDVMS):
            self.rdvms = pd.read_pickle(DATA_PATH_RDVMS)
        else:
            self.initializeRDVMs()

    def initializeRDVMs(self):
        d = {'Practice': [],
            'Address': [],
            'City': [],
            'ST': [],
            'Zip': [],
            'Ph1': [],
            'Ph2': [],
            'FAX': []}
        self.rdvms = pd.DataFrame(d)

    def updateRDVMs(self):
        self.loadRDVMs()
        self.updateClientRDVMs()
        self.practice.configure(values = list(self.rdvms.iloc[:,0]))
        self.onPracticeSelection()

    def rebuildTable(self):
        self.numEntries = len(self.data.values)
        self.listBox.delete(*self.listBox.get_children())
        for item in self.data.values:
            self.listBox.insert("", "end", values = list(item))
        self.listBox.configure(height = max(self.numEntries, 6))

    def updateClientRDVMs(self):
        clientData = self.data.drop(columns = ['RDVM phone 1', 'RDVM phone 2', 'RDVM fax'])
        rdvmData = self.rdvms[['Practice', 'Ph1', 'Ph2', 'FAX']]
        clientData = clientData.merge(rdvmData, how = 'left', on = 'Practice')
        clientData = clientData.rename(columns = {"Ph1" : "RDVM phone 1", "Ph2": "RDVM phone 2", "FAX": "RDVM fax"})
        noRDVM = clientData["RDVM phone 1"].isnull()
        clientData.loc[noRDVM, 'Practice'] = ''
        clientData.loc[noRDVM, 'RDVM phone 1'] = ''
        clientData.loc[noRDVM, 'RDVM phone 2'] = ''
        clientData.loc[noRDVM, 'RDVM fax'] = ''
        self.data = clientData
        self.saveData()
        self.rebuildTable()

    def onPracticeSelection(self, event = None):
        # The if exists to handle if the user deletes the rdvm currently selected
        if len(self.rdvms.loc[self.rdvms['Practice'] == self.practiceText.get()]) > 0:
            # In the case of multiple practice with the exact same name, just get the first one
            selection = self.rdvms.loc[self.rdvms['Practice'] == self.practiceText.get()].iloc[0, :]
            setText(self.rdvmPhone1, selection['Ph1'])
            setText(self.rdvmPhone2, selection['Ph2'])
            setText(self.rdvmFAX, selection['FAX'])
        else:
            self.practiceText.set('')
            setText(self.rdvmPhone1, '')
            setText(self.rdvmPhone2, '')
            setText(self.rdvmFAX, '')

    def saveData(self):
        saveData(self.data, DATA_PATH_CLIENT)

    def deleteDataItem(self, item):
        row = self.listBox.index(item)
        self.listBox.delete(item)

        self.numEntries -= 1
        self.listBox.configure(height = max(self.numEntries, 6))

        self.data = self.data.drop(self.data.index[row])

        self.clearFields()
        self.saveData()