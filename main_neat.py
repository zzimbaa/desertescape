from spelet.game import Game


def main():
    game = Game()
    print(game.world_data)  # tiles i spelet, det spelaren ser
    for player_pos in game.run(): #kappe gör så här fast med AI ;)
        #print(player_pos[1])
            game.moving_right = True
            game.jumping = True
            print(game._world.player.rightSensor)
        #print(f'player pos: {player_pos}')   # spelarens koordinater
        #print(f'game score: {game.score()}')  # score

main()
