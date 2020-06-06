from tkinter import *
from tkinter import ttk
from Echo import Echo
from Client import Client
from Studies import Studies
from RDVMs import RDVMs
from Print import Print

class Form(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.client = []

        f1 = Client(self)
        f1.pack(fill = X)

        f2 = Frame(self)
        self.studiesB = Button(f2, text = "Studies",
            command = lambda: self.changeTab(0))
        self.studiesB.grid(row = 0, column = 0)
        self.echoB = Button(f2, text = "Echo",
            command = lambda: self.changeTab(1))
        self.echoB.grid(row = 0, column = 1)
        self.rdvmsB = Button(f2, text = "RDVMs",
            command = lambda: self.changeTab(2))
        self.rdvmsB.grid(row = 0, column = 2)
        self.printB = Button(f2, text = "Print",
            command = lambda: self.changeTab(3))
        self.printB.grid(row = 0, column = 3)
        f2.pack(fill = X)

        self.studies = Studies(self)
        self.echo = Echo(self)
        self.rdvms = RDVMs(self)
        self.print = Print(self)
        self.tabs = [self.studies, self.echo, self.rdvms, self.print]

        self.buttons = [self.studiesB, self.echoB, self.rdvmsB, self.printB]
        self.button = self.rdvmsB
        self.button.configure(state = "disabled")

        self.tab = self.rdvms
        self.tab.pack(fill = X, pady = (10, 0))

    def updateClient(self, client):
        self.client = client
        self.echo.updateClient(self.client)

    def modifiedData(self, client):
        self.client = client
        self.echo.modifiedClient(self.client)

    def changeTab(self, tab):
        self.tab.pack_forget()
        self.tab = self.tabs[tab]
        self.tab.pack(fill = X, pady = (10, 0))

        self.button.configure(state = "active")
        self.button = self.buttons[tab]
        self.button.configure(state = "disabled")
