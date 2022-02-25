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


    
    
def main(genomes):
    hardcodedstart = 270
    game = Game()
    #world = game._world
    #players = world.playerList
    for player_pos in game.run():
        for nr, genome in enumerate(genomes):
            player = game._world.playerList[nr]
            sensors = {}
            sensors["1"] = 1/(player.rightSensor/10)
            genome.brain.makeReady()
            outputs = genome.brain.useNetwork(sensors)
            player.moving_right = outputs[0] > 0.5
            player.moving_left = outputs[1] > 0.5
            player.jump = outputs[2] > 0.5

    for nr, genome in enumerate(genomes):
        player = game._world.playerList[nr]
        # increase fitness for advancing in x position
        distance = max((player.rect.centerx - hardcodedstart, 0)) #Ifall skillnaden är negativ blir distance = 0
        genome.fitness = distance

def run():
    p = population.population()
    p.startPopulation()
    Time = #Hur mycket tid de ska få. Efter var femte generation typ så ge lite mer tid
    for i in range (0,10000):
        
        main(p.players)
        for i in p.players:
            if i.fitness > 1000:
                miscFuncs.drawNetwork(i.brain)
        p.nextGeneration()
run()