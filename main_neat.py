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

def main(players):
    print(len(players))
    for genome in players:
        #net = neat.nn.FeedForwardNetwork.create(g, config)
        #nets.append(net)
        genome.fitness = 0
        game = Game()
        xpos_max = 0
        score = 0
        for player_pos in game.run():
            print(game._world.player.rightSensor)
            # increase fitness for advancing in x position
            if player_pos[0] > xpos_max:
                genome.fitness += 1
                xpos_max = player_pos[0]

            # increase fitness for player score
            if game.score() > score:
                genome.fitness += (game.score() - score)
                score = game.score()

            # Use player position and world map as input
            sensors = {}
            sensors["1"] = game._world.player.rightSensor
            genome.brain.makeReady()
            outputs = genome.brain.useNetwork(sensors)
            game.moving_right = outputs[0] > 0.5
            game.moving_left = outputs[1] > 0.5
            game.jumping = outputs[2] > 0.5
            print(outputs)
    
    
    


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
