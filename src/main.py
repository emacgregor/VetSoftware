import pandas as pd
import os
from datetime import date
from os import path
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

DATA_DIR = '../data/'
DATA_PATH = DATA_DIR + 'data.pkl'
DEFAULT_COLUMN_WIDTH = 70
CLINICIANS = ["JMcG", "EMcG"]
RDVMS = ["Falmouth Veterinary Medicine"]

class Form(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.loadData()

        f1 = Frame(self)
        f1.pack(fill = X, padx = 10, pady = 10)

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
        self.clientNum.grid(row = 0,column = 2, padx = 2)
        self.patient = Text(f1, width = 12, height = 1)
        self.patient.grid(row = 1,column = 1, padx = 2)
        self.species = Text(f1, width = 12, height = 1)
        self.species.grid(row = 2,column = 1, padx = 2)
        self.breed = Text(f1, width = 12, height = 1)
        self.breed.grid(row = 2, column = 2, padx = 2)
        self.sex = Text(f1, width=4, height = 1)
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
        f2 = Frame(self)
        f2.pack(padx = 10)

        # Listbox all the basic pet information
        self.listBox = ttk.Treeview(f2, columns = list(self.data.columns), show = 'headings')
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

        # Scrollbars
        xsb = ttk.Scrollbar(f2,orient = HORIZONTAL, command = self.listBox.xview)
        ysb = ttk.Scrollbar(f2, orient = VERTICAL, command = self.listBox.yview)
        self.listBox.configure(xscrollcommand = xsb.set, yscrollcommand = ysb.set)
        self.listBox.grid(row = 0, column = 0,sticky = NSEW)
        ysb.grid(row = 0, column = 1,sticky = NS)
        xsb.grid(row = 1, column = 0,sticky = EW)
        f2.rowconfigure(0, weight = 1)
        f2.columnconfigure(0, weight = 1)

    def loadData(self):
        # Read data
        if path.exists(DATA_PATH):
            self.data = pd.read_pickle(DATA_PATH)
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

        self.saveData()

    def saveData(self):
        # Create the data folder if it doesn't exist
        if not path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        # Save data
        self.data.to_pickle(DATA_PATH)

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

    def fillFields(self, event):
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


# Create a GUI window
root = Tk()

# Set the background colour of GUI window, size, and name
root.configure()
root.title("Veterinary Software")
root.geometry("1000x500")

# Fills with the form information.
f1 = Form(root)
f1.pack()

# Start the GUI
root.mainloop()