
import copy
import math
from .species import species
from .history import connectionhistory
from .genome import genome
from .player import player
from . import config
class population():
    def __init__(self):
        self.species = []
        self.innoHistory = connectionhistory()
        self.players = []
        self.size = config.populations["size"]
        self.dropoffrate = config.populations["stale"]
    
    def putInSpecies(self):
        #ta bort alla individer i arterna (förutom reprentanten)
        for art in self.species:
            art.individer = []
        #Gå igenom varje player och kolla om de är kompatibel med någon av arterna annars skapa ny art
        for player in self.players:
            i = False
            for art in self.species:
                if art.isCompatiable(player.brain):
                    art.individer.append(player)
                    i = True
                    break 
            if i:
                continue
            #Ifall den kommer hit är den inte kompatibel med någon art --> ny art
            nyArt = species(player)
            self.species.append(nyArt)
            
    
    def sortSpecies(self): #sorterar arten på fitness
        self.species.sort(key=lambda x: (x.averageFit), reverse=True)

    #Tar hand om ett antal funktioner
    #för arterna
    def killHalfSpecies(self):
        for art in self.species:
            art.killHalf()
            art.sharedFitness() 
            art.averageFitness()

    def averageFitnessSumma(self):
        sum = 0
        for art in self.species:
            sum += art.averageFit
        return sum
    
    #Tar bort tomma arter
    def tommaSpecies(self):
        self.species = [x for x in self.species if not (len(x.individer) == 0)]

    #tar bort arter som inte har förbättrats
    def killDroppedOffSpecies(self):
        self.species = [x for x in self.species if not (x.dropOff == self.dropoffrate)]

    #Tar bort arter som inte kommer få några barn ändå
    def killBadSpecies(self):
        sum = self.averageFitnessSumma()
        self.species = [x for x in self.species if not (x.averageFit/sum * self.size < 1)]

    #Dåligt namn, sorterar bara alla individerna i arterna
    #Där högst fitness är högst upp
    def fitnessCalculation(self): 
        for art in self.species:
            art.sorteraArt()

    def nextGeneration(self):
        self.putInSpecies()
        self.tommaSpecies()
        self.fitnessCalculation() 
        self.killHalfSpecies()
        self.killDroppedOffSpecies()
        self.killBadSpecies()
        self.sortSpecies()

        barn = []

        averageSum = self.averageFitnessSumma()
        for art in self.species: 
            #Ha kvar de bästa indviderna från förra generationen
            barn.append(copy.deepcopy(art.best))
            #mängden barn den arten får -1 för den bästa redan är i arten
            amountOfChildren = math.floor(art.averageFit/averageSum * self.size - 1) 
            #Skapar barn
            for i in range(0, amountOfChildren):
                barn.append(art.createChild(self.innoHistory))
        #ifall det finns mer platser så ge mer barn till den bästa arten
        if len(barn) != self.size: 
            bestArt = self.species[0]
            antal = self.size - len(barn)
            for i in range(0,antal):
                barn.append(bestArt.createChild(self.innoHistory))
        self.players = barn
        

    def startPopulation(self):
        #Ger alla indivder i första generationen åtminstånde en anslutning
        for i in range(0,config.populations["size"]): 
            startBrain = genome()
            startBrain.initalizeNetwork()
            child = player(startBrain)
            child.brain.mutateConnection(self.innoHistory)
            self.players.append(child)
        self.nextGeneration()