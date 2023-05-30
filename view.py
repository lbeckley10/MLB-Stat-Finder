import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class View:

    #Constructor for the view
    def __init__(self):
        #Initially null the controller attribute
        self.controller = None

        #Create window
        self.root = tk.Tk()
        self.root.title("StatFinder")
        self.root.geometry("750x750")
        self.root.update()
        
        #Place widgets
        self.playerLabel = tk.Label(self.root, text="Enter a Player")
        self.playerLabel.grid(column=0, row=0, padx= 10, pady= 10, sticky="w")

        self.playerSearch = tk.Entry(self.root, width= int(self.root.winfo_width()/10))
        self.playerSearch.grid(column=0, row=1, padx= 10)

        self.yearLabel = tk.Label(self.root, text="Enter a Year")
        self.yearLabel.grid(column=0, row=2, padx= 10, pady= 10, sticky="w")

        self.yearSearch = tk.Entry(self.root, width= int(self.root.winfo_width()/10))
        self.yearSearch.grid(column=0,row=3, padx= 10)

        self.searchButton = tk.Button(self.root, width=int(self.root.winfo_width()/50), text="Search")
        self.searchButton.grid(column=1, row=1)

        self.imagePanel = tk.Label(text="IMAGE PLACEHOLDER")
        self.imagePanel.grid(column=0, row=4)

        #Place basic player info in a frame
        self.infoBox = tk.Frame()
        self.infoBox.grid(column=1, row=4)

        self.nameLabel = tk.Label(self.infoBox, text= "Name: ")
        self.nameLabel.grid(column= 0, row= 0)

        self.teamLabel = tk.Label(self.infoBox, text= "Team: ")
        self.teamLabel.grid(column= 0, row= 1)

        self.ageLabel = tk.Label(self.infoBox, text= "Age: ")
        self.ageLabel.grid(column= 0, row= 2)

        self.positionLabel = tk.Label(self.infoBox, text= "Position: ")
        self.positionLabel.grid(column= 0, row= 3)

        #Create frame that will contain stats
        self.statBox = tk.Frame()
        self.statBox.grid(column=0, row=5)
        self.statArray = [[None for i in range(2)] for j in range(17)]
        for i in range(17):
            for j in range(2):
                self.statArray[i][j] = tk.Label(self.statBox)
                self.statArray[i][j].grid(column = i, row = j)


        self.root.update()
        

    #Method to set the controller attribute.
    #@param controller is a reference to a controller object
    def setController(self, controller):
        self.controller = controller
        self.searchButton.config(command=self.controller.processClickEvent)
        self.root.mainloop()

    