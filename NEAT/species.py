#ordera genesen från början så slipper du göra det flera gånger
import random
from .genome import genome
from .history import connectionhistory
from .player import player
import numpy.random
import copy
from . import miscFuncs
import math
from . import config
class species():
    def __init__(self,best):
        self.best = best #Den bästa individen i artens genome
        self.individer = [best]
        self.averageFit = None
        self.dropOff = 0 #

    def averageFitness(self): #Dividebyzero
        totalfitness = 0
        for individ in self.individer:
            totalfitness += individ.fitness
        
        self.averageFit = totalfitness/(len(self.individer))
        #if self.averageFit == 1.5:
        #    ply = self.individer[0].brain
        #    print(totalfitness, " : ", len(self.individer), " : ", self.individer[0].fitness )
        #    print(len(self.individer[0].brain.connections))
        #    for i in ply.connections:
        #        print(ply.connections[i].weight)
        #    miscFuncs.drawNetwork(ply)
        #print(self.averageFit)
    def sorteraArt(self): #Sorterar arten där högst fitness är först/ ökar också dropOff
        self.individer.sort(key=lambda x: x.fitness, reverse=True)    
        if self.individer[0].fitness > self.best.fitness:
            self.dropOff = 0
            self.best = copy.deepcopy(self.individer[0]) #Är inte riktigt säker på om detta behövs?
        else:
            self.dropOff += 1
        
    def sharedFitness(self): #Förstår inte riktigt men tror detta gör att inte en art tar över hela populationen
        for individ in self.individer: #Försök göra detta på en radn för jag fattar inte hur man gör (how to run functon on attribute on all objects in list)
            individ.fitness = individ.fitness/len(self.individer)

            
   # def orderGenes(self, genes): #ger ordningen av generna där lägst innovationnumber går först, Gör till class variable
    #    #Varför behövs den här när gensen är i en dictionary?
     #   sorted_genes = copy.deepcopy(genes)
      #  sorted_genes.sort(key=lambda x: x.innovationnumber, reverse=False) 
       # return sorted_genes
    
    def createArray(self, genes, n):
        #geneDict = {}
        #for connection in genes:
        #    nr = connection.innovationnumber
        #    geneDict[str(id)] = True
        #Nu bör genes redan från början vara en dictionary?
        array = []
        for i in range(0, n+1):#Ska det vara n+1?
            if str(i) in genes:
                array.append(1)
            else:
                array.append(0)
        return array
    #Engligt pappret ska du få alla disjoin genes totalt. Varesig de är från genome 1 eller 2.
    #Rent tekniskt så ifall du vet antalet excess genes borde du ganska lätt kunna räkna ut antalet disjoint genes
    #Code bullet satte coeffcienten för disjoint och excess som samma.
    #Vad ifall du gör de två generna till en matris. Där raderna är genome1 och 2 och kolumner representerar en gene. Om en kolumn är 0 1 så betyder det att det är en disjoint.
    #Sen måste du lösa
    #utgå från att genes är sorterade
    def findDisjoinGenes(self, genes1, genes2): # på grund av att disjoint och excess har samma koeffcient behöver vi bara hitta totala mängden av båda och inte båda värdena enskilt 
        #vad ifall dem inte har några gener
        matching = 0
        for nr in genes1:
            if nr in genes2: #Betyder att båda har samma gen om det är true
                matching += 1
        disex = (len(genes1) - matching) + (len(genes2) - matching)
        return disex
#Lär finnas något mycket bättre sätt

    def weightDifference(self, genes1, genes2):
        count = 0
        total = 0
        lower = 0
        if len(genes1) == 0 or len(genes1) == 0: #går kanske att lägga ovanför?
                return 0
        for nr in genes1:
            if nr in genes2: #Betyder att båda har samma gen om det är true
                count += 1
                diff = abs(genes1[nr].weight - genes2[nr].weight)
                total += diff
        if count == 0: #Vad ska det bli om inga matchar? divide by zero
            return 100
        #print(total/count)
        return total/count

    #Kollar ifall genome är kompatibel till den arten
    def isCompatiable(self, testGenome):
        sGenome = self.best.brain
        disex = self.findDisjoinGenes(sGenome.connections, testGenome.connections)
        weightDiff = self.weightDifference(sGenome.connections, testGenome.connections) #Spelar ordningen roll?
        threshold = config.specie["compThreshold"]
        disExcCoefficent = config.specie["disJointCo"]
        weightDiffCoefficent = config.specie["weightDiffCoefficent"]
        factorN = 1
        if len(sGenome.connections) < 20 and len(testGenome.connections) < 20:
            factorN = 1 #the factor N, the number of genes in the larger genome, normalizes for genome size (N can be set to 1 if both genomes are small, i.e., consist of fewer than 20 genes). 
        else: 
            if len(sGenome.connections) < len(testGenome.connections):
                factorN = len(testGenome.connections)
            else:
                factorN = len(sGenome.connections)
        Delta = ((disExcCoefficent * disex)/factorN) + weightDiffCoefficent * weightDiff #Formel för att veta combatiblity från stanley papper
        if Delta > threshold:
            pass
            #print(disExcCoefficent * disex)
            #print(weightDiffCoefficent * weightDiff, "d")
        return Delta < threshold #DET SKA VARA Self.THRESHOLD ELLER NGT HÄR
    
    def tworandomIndivids(self):
        if len(self.individer) == 1: #Ifall det bara finns en indvid i arten får den inviden fortplanta med sig själv...
            return self.best, self.best
        n1, n2 = numpy.random.choice(self.individer, 2)
        if n2.fitness > n1.fitness:
            temp = n2
            n2 = n1
            n1 = temp        
        return n1, n2

    def selectPlayer(self):
        fitnessSum = 0
        for i in self.individer:
            fitnessSum += i.fitness

        randomFloat = random.uniform(0, fitnessSum)
        runSum = 0
        for i in self.individer:
            runSum += i.fitness
            if runSum > randomFloat:
                return i
    def createChild(self, history):
        #Genome1 ska ha högre eller lika med fitness med genome2
        #KODEN UNDER ANVÄNDS FLERA GÅNGER OCH GÅR ANTAGLIGEN ATT GÖRA OM TILL EN FUNKTION
        #genome1, genome2 = self.tworandomIndivids() #Tar två random grabbar
        genome1 = self.selectPlayer()
        genome2 = self.selectPlayer()
        if genome1.fitness < genome2.fitness:
            temp = genome1
            genome1 = genome2
            genome2 = temp
        genome1 = genome1.brain #tar deras hjärnor
        genome2 = genome2.brain
        genes1 = genome1.connections #Ordnar deras geneer
        genes2 = genome2.connections
        highest = 0
        #Behöver man ens ordra gensen? räcker det inte med len(genome1.connections)
        if len(genes1) == 0 and len(genes2) == 0:
            print("TESTAR3")
            #miscFuncs.drawNetwork(genome1)
            babyGenome = genome()
            babyGenome.initalizeNetwork()
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby
        elif len(genes1) == 0:
            print("TESTAR2")
            babyGenome = genome()
            babyGenome.connections = copy.deepcopy(genome2.connections)
            babyGenome.nodes = copy.deepcopy(genome2.nodes)
            babyGenome.layers = genome2.layers
            babyGenome.nextnode = genome2.nextnode
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby
        elif len(genes2) == 0:
            print("TESTAR1")
            babyGenome = genome()
            babyGenome.connections = copy.deepcopy(genome1.connections)
            babyGenome.nodes = copy.deepcopy(genome1.nodes)
            babyGenome.layers = genome1.layers
            babyGenome.nextnode = genome1.nextnode
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby
        #if genes1[-1].innovationnumber >= genes2[-1].innovationnumber:
        #    #detta ger inte lower eftersom du kommer ha dem i array
        #    highest = genes1[-1].innovationnumber
        #else:
        #    highest = genes2[-1].innovationnumber
        #Anta att du har två arrays
        #genes1 = self.createArray(genes1, highest)
        #genes2 = self.createArray(genes2, highest)
        babyGenes = {}
        for innonr in genome1.connections:
            #Ska du bara ta random vikt från föräldrer om det matchar?
            connection = genome1.connections[innonr]
            if innonr in genome2.connections: #Betyder att det matchar
                connection1 = genome2.connections[innonr]
                #ta randomly någons vikt. TAR OCKSÅ STATE (enabled/disabled)
                if random.random() <= 0.5:
                    #ta från genome1
                    babyGenes[innonr] = copy.deepcopy(connection)
                else:
                    babyGenes[innonr] = copy.deepcopy(connection1)
                if not connection1.enabled or not connection.enabled: 
                    if random.random() < 0.75:
                        babyGenes[innonr].enabled = False
                    else:
                        babyGenes[innonr].enabled = True
            else:   
                #Behåll alla genes från genome1
                babyGenes[innonr] = copy.deepcopy(connection)
            #Alla nodes från genome1 ges bara till barnet
        babyGenome = genome()
        babyGenome.connections = babyGenes
        babyGenome.nodes = copy.deepcopy(genome1.nodes)
        #DET ÄR FÖR DEN FORTPLANTAAR MED DET BÄSTA NÄTVERKET
        babyGenome.nextnode = genome1.nextnode
        #Kan vara layers som är problemet
        babyGenome.layers = genome1.layers
        babyGenome.mutate(history)
        baby = player(babyGenome)
        return baby


    def killHalf(self): #Dödar den sämre halvan av arten. Leta efter ett mer systematiskt sätt att döda av arten
        #Problemet med det här är att det kommer döda arter där det finns en kvar
        #https://stackoverflow.com/questions/15715912/remove-the-last-n-elements-of-a-list
        #https://stackoverflow.com/questions/50451570/how-to-divide-a-list-and-delete-half-of-it-in-python
        #Arten måste vara sorterad först
        #https://stackoverflow.com/questions/39471676/how-to-randomly-remove-a-percentage-of-items-from-a-list

        #den här funktionen tar bort 80% av alla arter indvider i arten oberonde av fitness 
        maxAntal = 2
        frac = 0.2

        antal = len(self.individer)

        haKvar = math.ceil(frac * antal)

        if haKvar == 1: #Så den bästa indivden har någon att fortplanta med
            haKvar = maxAntal

        self.individer = self.individer[:haKvar]
        #if len(self.individer) != 1:
        #    self.individer = self.individer[:len(self.individer)//2]
        

    