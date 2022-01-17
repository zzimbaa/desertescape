from matplotlib import pyplot as plt
from genome import genome
from node import Node
from connection import connection
from history import connectionhistory
import math
import miscFuncs
from population import population
import copy
pop = population()

pop.startPopulation()

pop.nextGeneration()
pop.nextGeneration()
pop.nextGeneration()
pop.nextGeneration()
pop.nextGeneration()
pop.nextGeneration()

lel = { }
lel["1"] = 1
for i in pop.species:
    for l in i.individer:
        if len(l.brain.connections) != 0:
            g = l.brain
        #g.makeReady()
        #print(g.useNetwork(lel))
            
o = pop.innoHistory

for innoNr,connection1 in enumerate(o.innovations):
    print(innoNr, connection1[0], connection1[1])

print(len(pop.species))