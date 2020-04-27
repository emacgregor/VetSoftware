import pandas as pd
from os import path
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

DATA_PATH = '../data/data.pkl'

if path.exists(DATA_PATH):
	data = pd.read_pickle(DATA_PATH)
else:
	d = {'Case number': [1],
		'Client number': [1],
		'Patient': ["test"],
		'Species': ["Canine"],
		'Breed': ["Labrador"],
		'Sex': ["Male"],
		'Birthdate': ["05/05/2005"],
		'Deathdate': ["05/05/2005"],
		'Client last': ["John"],
		'Client first': ["Doe"],
		'Clinician': ["test"],
		'City': ["test"],
		'State': ["NH"],
		'ZIP': ["55555"],
		'Home phone': ["555-555-5555"],
		'Work phone': ["555-555-5555"],
		'Alt phone': ["555-555-5555"],
		'RDVM last': ["John"],
		'RDVM first': ["Doe"],
		'Practice': ["test"],
		'RDVM phone 1': ["555-555-5555"],
		'RDVM phone 2': ["555-555-5555"],
		'RDVM fax': ["555-555-5555"]}
	data = pd.DataFrame(d)

# create a GUI window
root = Tk()

# set the background colour of GUI window
root.configure()
root.title("Veterinary Software")
root.geometry("1000x500")

f1 = Frame(root)
f1.pack(fill=X)

LEFT_LABEL_WIDTH = 16
RIGHT_LABEL_WIDTH = 18
ccNum = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="Case/Client #").grid(row=0, column=0)
client = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="Client").grid(row=1, column=0)
species = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="Species / Breed / Sex").grid(row=2, column=0)
birth = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="Birth / Death").grid(row=3, column=0)
la = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="LA / FU Date").grid(row=4, column=0)
clinic = Label(f1, anchor="w", width=LEFT_LABEL_WIDTH, text="Clinician").grid(row=5, column=0)
client = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="Client Last / First").grid(row=0, column=4)
city = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="City / ZIP / State").grid(row=1, column=4)
phone = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="Hm / Wk / Alt Phones").grid(row=2, column=4)
rdvm = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="RDVM Last / First").grid(row=3, column=4)
practice = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="Practice").grid(row=4, column=4)
rdvmphone = Label(f1, anchor="w", width=RIGHT_LABEL_WIDTH, text="RDVM Ph1 / Ph2 / FAX").grid(row=5, column=4)

# Define fields
field0_0 = Text(f1, width=12, height=1).grid(row=0, column=1, padx=2)
field0_1 = Text(f1, width=12, height=1).grid(row=0, column=2, padx=2)
field1 = Text(f1, width=12, height=1).grid(row=1, column=1, padx=2)
field2_0 = Text(f1, width=12, height=1).grid(row=2, column=1, padx=2)
field2_1 = Text(f1, width=12, height=1).grid(row=2, column=2, padx=2)
field2_2 = Text(f1, width=4, height=1).grid(row=2, column=3, padx=2)
field3_0 = DateEntry(f1).grid(row=3, column=1, padx=2)
field3_1 = DateEntry(f1).grid(row=3, column=2, padx=2)
field4_0 = DateEntry(f1).grid(row=4, column=1, padx=2)
field4_1 = DateEntry(f1).grid(row=4, column=2, padx=2)
field5 = ttk.Combobox(f1, width=12, values=["JMcG", "EMcG"]).grid(row=5, column=1, padx=2)
field6_0 = Text(f1, width=12, height=1).grid(row=0, column=5, sticky="w")
field6_1 = Text(f1, width=12, height=1).grid(row=0, column=5, sticky="w", padx=(105, 0))
field7_0 = Text(f1, width=12, height=1).grid(row=1, column=5, sticky="w")
field7_1 = Text(f1, width=12, height=1).grid(row=1, column=5, sticky="w", padx=(105, 0))
field7_2 = Text(f1, width=4, height=1).grid(row=1, column=5, sticky="w",  padx=(210, 0))
field8_0 = Text(f1, width=12, height=1).grid(row=2, column=5, sticky="w")
field8_1 = Text(f1, width=12, height=1).grid(row=2, column=5, sticky="w", padx=(105, 0))
field8_2 = Text(f1, width=12, height=1).grid(row=2, column=5, sticky="w", padx=(210, 0))
field9_0 = Text(f1, width=12, height=1).grid(row=3, column=5, sticky="w")
field9_1 = Text(f1, width=12, height=1).grid(row=3, column=5, sticky="w", padx=(105, 0))
field10_0 = ttk.Combobox(f1, width=31, values=["Falmouth Veterinary Medicine"]).grid(row=4, column=5, sticky="w")
field11_0 = Text(f1, width=12, height=1).grid(row=5, column=5, sticky="w")
field11_1 = Text(f1, width=12, height=1).grid(row=5, column=5, sticky="w", padx=(105, 0))
field11_2 = Text(f1, width=12, height=1).grid(row=5, column=5, sticky="w", padx=(210, 0))

# Submit button
submit = Button(f1, text="Submit", fg="Black")
submit.grid(row=6, column=5)

f2 = Frame(root)
f2.pack()

listBox = ttk.Treeview(f2,columns = list(data.columns), show='headings')
i = 0
for col in data.columns:
	listBox.heading(i, text=col)
	listBox.column(i, width=70)
	i += 1
for item in data.values:
	listBox.insert("", "end", values=list(item))
xsb = ttk.Scrollbar(f2,orient=HORIZONTAL, command=listBox.xview)
ysb = ttk.Scrollbar(f2, orient=VERTICAL, command=listBox.yview)
listBox.configure(xscrollcommand=xsb.set, yscrollcommand=ysb.set)
listBox.grid(row=0,column=0,sticky=NSEW)
ysb.grid(row=0,column=1,sticky=NS)
xsb.grid(row=1,column=0,sticky=EW)
f2.rowconfigure(0,weight=1)
f2.columnconfigure(0,weight=1)

# start the GUI
root.mainloop()

data.to_pickle(DATA_PATH)