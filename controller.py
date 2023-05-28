from model import Model
from view import *
from search import *

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    #Updates the playerBox attribute of the model
    def updatePlayerBox(self, player):
        self.model.playerBox = player
    
    #Updates the yearBox attribute of the model
    def updateYearBox(self, year):
        self.model.yearBox = year
    
    #Updates the basic info attributes of the model
    def updateInfo(self, name, team, age, position):
        self.model.name = name
        self.model.team = team
        self.model.age = age
        self.model.position = position
    
    #Updates the stats attribute of the model
    def updateStats(self, stats):
        self.model.stats = stats
    
    #Updates the view to match the model
    def updateView(self):
        self.view.nameLabel.config(text= f"Name: {self.model.name}")
        self.view.ageLabel.config(text=f"Age: {self.model.age}")
        self.view.teamLabel.config(text=f"Team: {self.model.team}")
        self.view.positionLabel.config(text=f"Position: {self.model.position}")
        keys = list(self.model.stats.keys())
        for i in range(17):
            print(keys[i])
            self.view.statBox[0][i].config(text= str(keys[i]))
            self.view.statBox[1][i].config(text= str(self.model.stats.get(keys[i])))
        self.view.root.update()

    #Conducts search and updates model when the button is clicked
    def processClickEvent(self):
        self.updatePlayerBox(self.view.playerSearch.get())
        self.updateYearBox(self.view.yearSearch.get())
        self.updateStats(Search.statSearch(self.model.playerBox, self.model.yearBox))
        print(type(self.model.stats))
        self.updateInfo(self.model.playerBox, self.model.stats.get("team"), self.model.stats.get("age"), self.model.stats.get("position"))
        self.updateView()
