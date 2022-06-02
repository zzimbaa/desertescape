from spelet.game import Game
from NEAT import population
from NEAT import config
from NEAT import connection
from NEAT import genome
from NEAT import history
from NEAT import miscFuncs
from NEAT import node
from NEAT import player
from NEAT import species
from spelet.player import Player
from matplotlib import pyplot as plt
import copy

def main(genomes,time):
    hardcodedstart = 270
    game = Game()
    done = False
    for furthest_player in game.run(time,genomes):
        for nr, genome in enumerate(genomes):
            player = game._world.playerList[nr]
            sensors = {}
            sensors["1"] = player.sensors[0]
            sensors["2"] = player.sensors[1]
            sensors["3"] = player.sensors[2]
            genome.brain.makeReady()
            outputs = genome.brain.useNetwork(sensors)
            player.moving_right = outputs[0] > 0.5
            player.moving_left = outputs[1] > 0.5
            player.jump = outputs[2] > 0.5

    for nr, genome in enumerate(genomes):
        player = game._world.playerList[nr]
        # increase fitness for advancing in x position
        distance = max((player.rect.centerx + game._world.bg_scroll) - hardcodedstart, 0) #Ifall skillnaden är negativ blir distance = 0
        player.network = genome
        player.distance = distance
        genome.fitness = round(distance/60) 
        if player.victory:
            genome.fitness += 100
            print(player.completeTime)
            done = True
    best = sorted(game._world.playerList, key=lambda x: x.network.fitness, reverse=True)[0]
    fitness = best.network.fitness
    network = copy.deepcopy(best.network)
    time = best.completeTime
    playerList = [fitness, network, time]
    return best, done
    
def run():
    p = population.population()
    p.startPopulation()
    Time = 0 #Hur mycket tid de ska få. Efter var femte generation typ så ge lite mer tid
    gen = 0 #Vilken Generation den är på
    #bestPlayers = []
    bestplayer = None
    for i in range (0,1000):
        if (i % 5) == 0 and Time != 25:
            Time += 6
        #Kod för data om hur individernas utveckling
        #bestPlayer, state = main(p.players,Time)
        #bestPlayers.append(bestPlayer)
        bestPlayer, state = main(p.players,Time)
        #Ifall en individ har klarat det sluta loopa
        if state: 
            break
        p.nextGeneration()
        gen += 1
    solutionData(gen, bestPlayer)

def solutionData(gens, bestplayer):
    bestplayer = bestplayer.network.brain
    neurons = len(bestplayer.nodes) #Ger antal neuroner
    active_connections = 0 
    #Ger antalet aktiva gener i lösning
    for i in bestplayer.connections:
        if bestplayer.connections[i]:
            active_connections += 1
    #printar datan efter lösning hittas
    print(f"Antal gömda neuroner: {neurons-7}")
    print(f"Antal aktiverade anslutningar: {active_connections}")
    print(f"Antal generationer för att hitta en lösning: {gens}")
    
    
#Funktion för att skriva ner hur 
#indviderna lyckades från början till slut
#Inte särskillt intressant
def drawData(gen, bestPlayers):
    fitnesses = [bestPlayer[0] for bestPlayer in bestPlayers]
    brains = [bestPlayer[1].brain for bestPlayer in bestPlayers]
    times = [bestPlayer[2] for bestPlayer in bestPlayers]
    gens = [x+1 for x in range(gen)]
    neurons = [len(network.nodes) for network in brains]
    connections = [len(network.connections) for network in brains]
    #Gör en fil med fitness data
    with open('fitness.txt', 'x') as f:
        for item in fitnesses:
            f.write("%s\n" % item)
    #Gör en fil med Neuron data
    with open('neuron.txt', 'x') as f:
        for item in neurons:
            f.write("%s\n" % item)
    #Gör en fil med Neuron data
    with open('conns.txt', 'x') as f:
        for item in connections:
            f.write("%s\n" % item)
    

run()