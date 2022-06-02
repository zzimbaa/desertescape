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
        #Den bästa individen i artens
        #Också individen som representerar arten
        self.best = best 
        self.individer = [best]
        self.averageFit = None
        self.dropOff = 0 

    def averageFitness(self): 
        totalfitness = 0
        for individ in self.individer:
            totalfitness += individ.fitness
        self.averageFit = totalfitness/(len(self.individer))
        
    #Sorterar arten där individ med högst fitness är först 
    #ökar/tar bort dropOff
    def sorteraArt(self): 
        self.individer.sort(key=lambda x: x.fitness, reverse=True)    
        #Om en individ är bättre än den som förut var bäst
        #sätts dropoff till 0 och indviden blir den nya bästa
        if self.individer[0].fitness > self.best.fitness:
            self.dropOff = 0
            self.best = copy.deepcopy(self.individer[0]) 
        else:
            self.dropOff += 1
    
    #För att en art inte ska ta över helt delas
    #alla indviders fitness med antalet indvider i arten
    def sharedFitness(self): 
        for individ in self.individer: 
            individ.fitness = individ.fitness/len(self.individer)


    def findDisjoinGenes(self, genes1, genes2): 
        #på grund av att disjoint och excess har samma koeffcient behöver vi bara hitta totala mängden av båda och inte båda värdena enskilt
        matching = 0
        for nr in genes1:
            if nr in genes2: #Betyder att båda har samma gen om det är sant
                matching += 1
        disex = (len(genes1) - matching) + (len(genes2) - matching)
        return disex

    def weightDifference(self, genes1, genes2):
        count = 0
        total = 0
        lower = 0
        if len(genes1) == 0 or len(genes1) == 0: 
                return 0
        for nr in genes1:
            if nr in genes2: #Betyder att båda har samma gen om det är sant
                count += 1
                diff = abs(genes1[nr].weight - genes2[nr].weight)
                total += diff
        if count == 0: 
            return 100
        return total/count

    #Kollar ifall genome är kompatibel till den arten
    def isCompatiable(self, testGenome):
        sGenome = self.best.brain
        disex = self.findDisjoinGenes(sGenome.connections, testGenome.connections)
        weightDiff = self.weightDifference(sGenome.connections, testGenome.connections)
        threshold = 3
        disExcCoefficent = 1
        weightDiffCoefficent = 0.5
        factorN = 1
        #the factor N, the number of genes in the larger genome, normalizes for genome size 
        #(N can be set to 1 if both genomes are small, i.e., consist of fewer than 20 genes).
        if len(sGenome.connections) < 20 and len(testGenome.connections) < 20:
            factorN = 1  
        else: 
            if len(sGenome.connections) < len(testGenome.connections):
                factorN = len(testGenome.connections)
            else:
                factorN = len(sGenome.connections)
        Delta = ((disExcCoefficent * disex)/factorN) + weightDiffCoefficent * weightDiff #Formel för att veta combatiblity från stanley papper
        return Delta < threshold 
    
    #Tar fram en delvis slumpmässig indvid
    #Större chans att individen har större fitness
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
        if len(genes1) == 0 and len(genes2) == 0:
            babyGenome = genome()
            babyGenome.initalizeNetwork()
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby
        elif len(genes1) == 0:
            babyGenome = genome()
            babyGenome.connections = copy.deepcopy(genome2.connections)
            babyGenome.nodes = copy.deepcopy(genome2.nodes)
            babyGenome.layers = genome2.layers
            babyGenome.nextnode = genome2.nextnode
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby
        elif len(genes2) == 0:
            babyGenome = genome()
            babyGenome.connections = copy.deepcopy(genome1.connections)
            babyGenome.nodes = copy.deepcopy(genome1.nodes)
            babyGenome.layers = genome1.layers
            babyGenome.nextnode = genome1.nextnode
            babyGenome.mutate(history)
            baby = player(babyGenome)
            return baby

        babyGenes = {}
        for innonr in genome1.connections:
            connection = genome1.connections[innonr]
            if innonr in genome2.connections: 
                randomnr = random.choice([0, 1])
                #ta slumpmässigt någons vikt.
                if randomnr == 0:
                    #ta från genome1
                    babyGenes[innonr] = copy.deepcopy(connection)
                else:
                    babyGenes[innonr] = copy.deepcopy(genome2.connections[innonr])
            else:
                #Behåll alla gener från genome1
                babyGenes[innonr] = copy.deepcopy(connection)
        #Alla nodes från genome1 ges till barnet
        babyGenome = genome()
        babyGenome.connections = babyGenes
        babyGenome.nodes = copy.deepcopy(genome1.nodes)
        babyGenome.nextnode = genome1.nextnode
        babyGenome.layers = genome1.layers
        babyGenome.mutate(history)
        baby = player(babyGenome)
        return baby

    #den här funktionen tar bort 80% av alla individer i arten 
    #alltså top 20% är kvar
    def killHalf(self): 
        maxAntal = 2
        frac = 0.2
        antal = len(self.individer)
        haKvar = math.ceil(frac * antal)
        if haKvar == 1: #Så den bästa indivden har någon att fortplanta med
            haKvar = maxAntal
        self.individer = self.individer[:haKvar]


