from spelet.game import Game
from neat import population
from neat import config
from neat import connection
from neat import genome
from neat import history
from neat import miscFuncs
from neat import node
from neat import player
from neat import species
#from NEAT import miscFuncs


    
    
def main(genomes):
    hardcodedstart = 270
    game = Game()
    world = game._world
    players = world.playerList
    for player_pos in game.run():
        for nr, genome in enumerate(genomes):
            player = players[nr]
            sensors = {}
            sensors["1"] = player.rightSensor
            genome.brain.makeReady()
            outputs = genome.brain.useNetwork(sensors)
            player.moving_right = outputs[0] > 0.5
            player.moving_left = outputs[1] > 0.5
            player.jumping = outputs[2] > 0.5

    for nr, genome in enumerate(genomes):
        player = players[nr]
        # increase fitness for advancing in x position
        distance = max((player.rect.centerx - hardcodedstart, 0)) #Ifall skillnaden är negativ blir distance = 0
        genome.fitness = distance

def run():
    p = population.population()
    p.startPopulation()
    for i in range (0,10000):
        
        main(p.players)
        for i in p.players:
            if i.fitness > 1000:
                miscFuncs.drawNetwork(i.brain)
        p.nextGeneration()
run()
