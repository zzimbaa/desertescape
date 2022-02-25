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
#from NEAT import miscFuncs


    
    
def main(genomes,time):
    hardcodedstart = 270
    game = Game()
    #world = game._world
    #players = world.playerList
    for player_pos in game.run(time):
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
        genome.fitness = round(distance/60) #Blir nog lättare att beräkna om det är int
        if player.victory:
            genome.fitness += 100
            print(player.completeTime)
    alive_players = sorted(genomes, key=lambda x: x.fitness, reverse=True)
    print(alive_players[0].fitness)
    #Hur ska fitness ges ut
def run():
    p = population.population()
    p.startPopulation()
    Time = 0 #Hur mycket tid de ska få. Efter var femte generation typ så ge lite mer tid
    for i in range (0,10000):
        if (i % 10) == 0 and Time != 20:
            Time += 5
        print(Time)
        main(p.players,Time)
        for i in p.players:
            if i.fitness > 1000:
                miscFuncs.drawNetwork(i.brain)
        p.nextGeneration()
run()