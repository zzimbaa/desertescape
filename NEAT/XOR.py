import random
from matplotlib import pyplot as plt
#from genome import genome
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

global solutio 
global times 
solutio = 0
times = 0
def XOR():
    antalNodes = 0
    pop = population()
    pop.startPopulation()
    shuffled = random.sample(xor,4)
    print(shuffled)
    print(shuffled[0])
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
                #print(output)
            for i in range(0,4):
                #print(shuffled[i][2] - outputs[i])
                player.fitness -= (outputs[i] - shuffled[i][2]) ** 2
            #print(player.fitness)
            if player.fitness > 3.95:
                for i in pop.innoHistory.innovations:
                    print(i[0], " to ", i[1])
                input = {}
                input["1"] = 1
                input["2"] = 1
                output1 = brain.useNetwork(input)[0]

                input["1"] = 0
                input["2"] = 0
                output2 = brain.useNetwork(input)[0]

                input["1"] = 0
                input["2"] = 1
                output3 = brain.useNetwork(input)[0]

                input["1"] = 1
                input["2"] = 0
                output4 = brain.useNetwork(input)[0]
                print(output1)
                print(output2)
                print(output3)
                print(output4)
                print(gen)
                antalNodes = len(brain.nodes) - 4
                i = False
                break
            #if gen == 100:
            #    miscFuncs.drawNetwork(brain)
        if not i:
            pass
            #XOR()
        pop.nextGeneration()
        gen += 1
    return antalNodes

sum = 0
for l in range(1,101):
    sum += XOR()
    print(sum/l)
print(sum/101)
#För någon anledning blir det 1,5 i konsolen hela tiden (varför?)
#Den håller på väldigt länge med att inte ha gener överhuvudtaget
#Gör om så när den muterar nodes så får de två nya connections samma vikt som den disablade
#Du har fortfarande igång så den inte kan mutera mer än en node
#Antagligen är problemet att den inte utvecklas tillräckligt snabbt
#Testa att öka dropoff
#Utforska om varför average fitness inte verkar gå upp
#Lägg på remove mutatations
#1−∑i(ei−ai)2 e expected | a acutal

#Jag har kommit fram till att det är möjligt att få en 3.95 lösning med två extra noder (3.96 hittades också med 2 noder) (3.97) (3.98 också) (3.99)

#En art som är skit bra dör fortfarande