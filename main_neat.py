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
#from NEAT import miscFuncs
from matplotlib import pyplot as plt
import copy
    
    
def main(genomes,time):
    hardcodedstart = 270
    game = Game()
    #world = game._world
    #players = world.playerList
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
        genome.fitness = round(distance/60) #Blir nog lättare att beräkna om det är int
        if player.victory:
            genome.fitness += 100
            print(player.completeTime)
    best = sorted(game._world.playerList, key=lambda x: x.network.fitness, reverse=True)[0]
    fitness = best.network.fitness
    network = copy.deepcopy(best.network)
    time = best.completeTime
    playerList = [fitness, network, time]
    return playerList
    
def run():
    p = population.population()
    p.startPopulation()
    Time = 0 #Hur mycket tid de ska få. Efter var femte generation typ så ge lite mer tid
    gen = 1 #Vilken Generation den är på
    bestPlayers = []
    for i in range (0,2):
        if (i % 10) == 0 and Time != 20:
            Time += 5
        #print(Time)
        bestPlayer = main(p.players,Time)
        bestPlayers.append(bestPlayer)
        p.nextGeneration()
    drawData(gen, bestPlayers)
    
def drawData(gen, bestPlayers):
    fitnesses = [bestPlayer.network.fitness for bestPlayer in bestPlayers]
    brains = [bestPlayer.network.brain for bestPlayer in bestPlayers]
    times = [bestPlayer.completeTime for bestPlayer in bestPlayers]
    gens = [x+1 for x in range(gen+1)]
    fitnessGraph = zip(gens, fitnesses)
    print(gens)
    print(gens)
    plt.plot(gens, fitnesses)
    plt.show()

run()