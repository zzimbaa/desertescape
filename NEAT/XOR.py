import random
from matplotlib import pyplot as plt
from node import Node
from connection import connection
from history import connectionhistory
import math
import miscFuncs
from population import population
import copy


xor = [[0,0,0],
    [0,1,1],
    [1,0,1],
    [1,1,0]]


def XOR():
    antalNodes = 0
    fitness_threshold = 3.95
    pop = population()
    pop.startPopulation()
    shuffled = random.sample(xor,4)
    gen = 1
    i = True
    while i:
        shuffled = random.sample(xor,4)
        for player in pop.players:
            outputs = []
            player.fitness = 4
            player.correct = 0
            for bits in shuffled:
                bit1 = bits[0]
                bit2 = bits[1]
                answer = bits[2]
                input = {}
                input["1"] = bit1
                input["2"] = bit2
                brain = player.brain  
                brain.makeReady()
                output = brain.useNetwork(input)[0]
                outputs.append(output)


            for i in range(0,4):
                player.fitness -= (outputs[i] - shuffled[i][2]) ** 2

            if player.fitness > fitness_threshold: 
                antalConnections = 0
                #Antal aktiva anslutningar
                for connection in brain.connections:
                    if brain.connections[connection].enabled:
                        antalConnections += 1
                #Antal gömda neuroner
                antalNodes = len(brain.nodes) - 4
                i = False
                #ifall lösning är funnen avsluta while loopen
                break
        pop.nextGeneration()
        gen += 1
    return antalNodes, gen, antalConnections

sum = 0
gens = 0
conns = 0
#Kör XOR testet 100 gånger och efteråt
#printar ut resultatet
for l in range(1,101):
    t, p, l = XOR()
    sum += t
    gens += p
    conns += l
print(sum/100)
print(gens/100)
print(conns/100)
