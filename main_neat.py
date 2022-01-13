import random
import itertools
from spelet.game import Game


def main():
    game = Game()
    world_data = tuple(itertools.chain(*game.world_data))
    print(world_data)  # tiles i spelet, det spelaren ser
    for player_pos in game.run(): #kappe gör så här fast med AI ;)
        if player_pos[0] < 800:
            game.moving_right = True
        elif player_pos[0] < 1100:
            game.moving_right = True
            game.jumping = True
        elif player_pos[0] < 1500:
            game.moving_right = True
            game.jumping = False
        elif player_pos[0] < 1600:
            game.moving_right = True
            game.jumping = True
        elif player_pos[0] < 2500:
            game.moving_right = True
            game.jumping = False
        elif player_pos[0] < 2700:
            game.moving_right = True
            game.jumping = True
        else:
            game.moving_right = True
            game.jumping = False
        print(f'player pos: {player_pos}')   # spelarens koordinater
        print(f'game score: {game.score()}')  # score

main()
