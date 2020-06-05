from tkinter import *
from tkinter import ttk
from Echo import Echo
from Client import Client

class Form(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.client = []

        f1 = Client(self)
        f1.pack(fill = X)

        self.tab = Echo(self)
        self.tab.pack(fill = X)

    def updateClient(self, client):
        self.client = client
        self.tab.updateClient(self.client)

    def modifiedData(self, client):
        self.client = client
        self.tab.modifiedClient(self.client)